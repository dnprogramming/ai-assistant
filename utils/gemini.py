import pathlib
import textwrap
import google.generativeai as genai
from IPython.display import display
from IPython.display import Markdown

from config import config

genai.configure(api_key=config.Config().gemini_api_key)
model = genai.GenerativeModel("gemini-pro")


class gemini:

    def generate_text(prompt):
        question = (
            "Please get the description, subject, and date as a datetime in iso format for the meeting. The date in the email will be in mm-dd-yyyy format and please separate each of the three fields with a pipe character like this format: subject|description|date. The email states: "
            + prompt
        )
        response = model.generate_content(question)
        text = response.text.replace("•", "")
        return text

    def translate(prompt):
        question = prompt
        response = model.generate_content(question)
        text = response.text
        return text

    def question(prompt):
        question = prompt
        response = model.generate_content(question)
        text = response.text
        return text
