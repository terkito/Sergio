"""
Cloud Function for getting text response from Gemini API.
(Required for parallel image generation)
"""

# pylint: disable=E0401

import os

from dotenv import load_dotenv
import functions_framework
from vertexai.preview import generative_models
from vertexai.preview.generative_models import GenerativeModel

load_dotenv()

PROJECT_ID = os.getenv("PROJECT_ID")
LOCATION = os.getenv("LOCATION")


def generate_text(prompt: str):
    """Generates text using the Gemini-Pro model.

    Args:
        prompt: The text prompt to use for generation.

    Returns:
        The generated text.
    """
    model = GenerativeModel("gemini-pro")
    safety_setting = generative_models.HarmBlockThreshold.BLOCK_NONE

    responses = model.generate_content(
        prompt,
        generation_config={
            "max_output_tokens": 2048,
            "temperature": 0.001,
            "top_p": 1,
        },
        safety_settings={
            generative_models.HarmCategory.HARM_CATEGORY_HATE_SPEECH: safety_setting,
            generative_models.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: safety_setting,
            generative_models.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: safety_setting,
            generative_models.HarmCategory.HARM_CATEGORY_HARASSMENT: safety_setting,
        },
        stream=True,
    )
    final_response = ""
    for response in responses:
        final_response += response.text
    return final_response


@functions_framework.http
def generate_text_http(request):
    """HTTP Cloud Function that generates text using the Gemini-Pro model.

    Args:
        request (flask.Request): The request object.
        <http://flask.palletsprojects.com/en/1.1.x/api/#incoming-request-data>

    Returns:
        The response text, or any set of values that can be turned into a
        Response object using `make_response`
        <http://flask.palletsprojects.com/en/1.1.x/api/#flask.make_response>.
    """
    request_json = request.get_json(silent=True)
    if not request_json or "text_prompt" not in request_json:
        return {"error": "Request body must contain 'text_prompt' field."}, 400

    text_prompt = request_json["text_prompt"]
    generated_text = generate_text(text_prompt)

    return {"generated_text": generated_text}