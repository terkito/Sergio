import base64
import json
import os
import sys
import urllib.request

import requests
import vertexai.preview.generative_models as generative_models

sys.path.append("../")
from config import config
from genai_prompts import qList, qList2
from helper_functions_insta import get_id
from vertexai.preview.generative_models import GenerationConfig, GenerativeModel, Part
from vertexai.preview.language_models import TextGenerationModel
from vertexai.preview.vision_models import Image, ImageQnAModel

gemini_model: GenerativeModel = GenerativeModel("gemini-1.0-pro-vision-001")
gemini_model_language: GenerativeModel = GenerativeModel("gemini-1.0-pro-002")

parameters = config["parameters"]["standard"]


fewshot_images: list[Part] = []
num_files = len(config["fewshot_images"])
for i in range(num_files):
    filename = "image" + str(i + 1)
    fewshot_images.append(Part.from_uri(config["fewshot_images"][filename]), mime_type="image/jpeg"))


def generate_caption(image_path: str) -> dict:
    """Generates a caption for an image using the Gemini model.

    Args:
                    image_path (str): The path to the image file.

    Returns:
                    dict: A dictionary containing the generated caption.
    """

    answer: dict = {}

    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
        user_image = Part.from_data(
            data=base64.b64decode(encoded_string), mime_type="image/jpeg"
        )

    prompt = [
        """
                You are a fashion editor and your task is to spot fashion trends and extract outfit and fashion items from the image provided .
                List all outfit items in list of json format, with separate json for each person in the input image.
                Be as detailed as possible listing shapes, texture, material, length, design pattern, design description and brands.
                If there is no person in the image, return an empty list and only mention items that are visible in the image.
                Use fashion terminology if possible and be verbose."""
        """Input image:""",
        fewshot_images[0],
        """Output:
    [
        {
            \"hat\": \"curved brim cotton red yankees baseball cap\",
            \"sunglasses\": \"black small aviators \",
            \"jacket\": \"black bomber waist length leather jacket\",
            \"shirt\": \"white crew neck cotton t-shirt\",
            \"pants\": \"cotton chinos full length straight leg beige pants\"
        },
        {
            \"jacket\": \"cropped bomber green and white waist height  louis vuitton jacket\",
            \"shirt\": \"white cotton crop top\",
            \"skirt\": \"gabardine a-line beige mini skirt\",
            \"socks\": \"white sheer ankle crew socks\",
            \"bag\": \"green small rectangular leather top handle shoulder bag\"
        }
    ]


    Input image:""",
        fewshot_images[1],
        """Output:
[
        {
            \"top\": \"brown leopard print mid length cotton top with a square neckline and balloon sleeves and button-up front\",
            \"jeans\": \"high-waisted,  mid-rise, straight-leg style, light-wash ripped distressed denim jeans\",
            \"bag\": \"white leather rectangular tote bag\",
            \"sunglasses\": \"black cat eye style square sunglasses\",
            \"accessories\": \"choker gold necklace\"
            \"accessories\": \"choker bangle  bracelet\"
        }
]

    Input image:""",
        user_image,
        """Output:""",
    ]

    response = gemini_model.generate_content(
        prompt,
        generation_config=GenerationConfig(
            max_output_tokens=2048,
            temperature=0.4,
            top_p=1,
            top_k=32,
        ),
        safety_settings={
            generative_models.HarmCategory.HARM_CATEGORY_HATE_SPEECH: generative_models.HarmBlockThreshold.BLOCK_ONLY_HIGH,
            generative_models.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: generative_models.HarmBlockThreshold.BLOCK_ONLY_HIGH,
            generative_models.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: generative_models.HarmBlockThreshold.BLOCK_ONLY_HIGH,
            generative_models.HarmCategory.HARM_CATEGORY_HARASSMENT: generative_models.HarmBlockThreshold.BLOCK_ONLY_HIGH,
        },
        stream=False,
    ).text

    try:
        response = json.loads(response)
    except Exception as e:
        print(e)
        return {}

    for json_ob in response:
        for category in json_ob.keys():
            if category in answer:
                answer[category].append(json_ob[category])
            else:
                answer[category] = [json_ob[category]]

    return answer


def get_posts(user: str, previous: list, cnt: int = 10, cookies: dict = {}) -> list:
    """Gets a list of posts from an Instagram user.

    Args:
                    user (str): The username of the Instagram user.
                    previous (list): A list of previous posts.
                    cnt (int): The number of posts to get.
                    cookies (dict): A dictionary of cookies.
                    model (str): The model to use for generating the captions.

    Returns:
                    list: A list of posts.
    """

    org_cnt = cnt
    userId = get_id(user, cookies)
    if userId is None:
        return previous
    params = {
        "query_id": config["postid"],  # Fixed value for posts
        "id": userId,  # User ID
        "first": 12,
    }

    if len(previous) != 0:
        latest_id = previous[0][0]
    else:
        latest_id = ""

    print("latest id: ", latest_id, "\n")
    posts = []

    flag = False
    while cnt > 0 and flag is False:
        response = requests.get(
            config["links"]["graphql"], params=params, cookies=cookies
        )

        print(response.status_code)

        if response.status_code != 200:
            print(response)
            break

        parsed_data = json.loads(response.text)

        media = parsed_data["data"]["user"]["edge_owner_to_timeline_media"]

        for i in range(len(media["edges"])):
            if media["edges"][i]["node"]["__typename"] == "GraphVideo":
                continue

            postid = media["edges"][i]["node"]["id"]
            postlink = media["edges"][i]["node"]["display_url"]
            print("post id: ", postid)

            if postid == latest_id:
                flag = True
                break

            actual_img_path = "" + user + "$.png"
            urllib.request.urlretrieve(postlink, actual_img_path)

            try:
                caption = generate_caption(actual_img_path)
            except Exception as e:
                print(e)
            else:
                posts = [(postid, postlink, caption)] + posts  # newest post stays first
                cnt -= 1
            finally:
                os.remove(actual_img_path)

            if cnt == 0:
                break

        params["after"] = media["page_info"]["end_cursor"]

    posts = posts + previous
    if len(posts) > org_cnt:
        posts = posts[:org_cnt]

    print("final cnt = ", cnt)
    return posts


def summarize_article(article_text: str) -> str:
    """Summarizes an article.

    Args:
                    article_text (str): The article text.

    Returns:
                    str: The summary.
    """

    response = gemini_model_language.generate_content(
        [f"Provide a brief summary for the following article: {article_text}"],
        generation_config=GenerationConfig(
            max_output_tokens=2048,
            temperature=1,
            top_p=1,
        ),
        safety_settings={
            generative_models.HarmCategory.HARM_CATEGORY_HATE_SPEECH: generative_models.HarmBlockThreshold.BLOCK_ONLY_HIGH,
            generative_models.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: generative_models.HarmBlockThreshold.BLOCK_ONLY_HIGH,
            generative_models.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: generative_models.HarmBlockThreshold.BLOCK_ONLY_HIGH,
            generative_models.HarmCategory.HARM_CATEGORY_HARASSMENT: generative_models.HarmBlockThreshold.BLOCK_ONLY_HIGH,
        },
        stream=False,
    )

    return response.text
