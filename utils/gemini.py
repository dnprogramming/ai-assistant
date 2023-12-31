import pathlib
import textwrap
import google.generativeai as genai
from IPython.display import display
from IPython.display import Markdown

from config import config

genai.configure(api_key=config.Config().gemini_api_key)
model = genai.GenerativeModel('gemini-pro')

class gemini:
    def generate_text(prompt):
        question = "Please get the description, subject, and date of the meeting: " + prompt
        response = model.generate_content(question)
        text = response.text.replace('•', '  *')
        print(response)
        return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))
