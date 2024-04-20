import json
import os

from config import config
from dataProcessing import generateCaption
from driver import get_top_categories

data_path = config["Data"]["current_data"]


def imagesScrape(saved):
    """

    Write code here to extract/ scrape images from your data source.
    For each image, store it in your local directory (same path as this file)
    Then, for each image, call generateCaption() function written in dataProcessing.py which returns a dictionary
    Store the results in an array to finally get an array of dictionaries

    Dummy code for two locally stored images -
    """

    answers = []
    image_files = os.listdir("gemini_fewshot_images")
    for image_file in image_files:
        image_path = os.path.join("gemini_fewshot_images", image_file)

        print(image_path)
        answer = generateCaption(image_path, "Gemini")
        answers.append(answer)

    saved["finaldata"] = {}
    saved["finaldata"]["All countries"] = {}

    for image_attr in answers:
        for cat in image_attr:
            if cat in saved["finaldata"]["All countries"]:
                saved["finaldata"]["All countries"][cat].extend(image_attr[cat].copy())
            else:
                saved["finaldata"]["All countries"][cat] = image_attr[cat].copy()

    with open(data_path, "w") as outfile:
        json.dump(saved, outfile)

    get_top_categories(saved)


def articlesScrape():
    pass


if __name__ == "__main__":
    with open(data_path, "r") as f:
        saved = json.load(f)

    # call either one or both functions to replace the current data
    # first function is for images scrape and second is for articles scrape

    imagesScrape(saved)
    # articlesScrape()