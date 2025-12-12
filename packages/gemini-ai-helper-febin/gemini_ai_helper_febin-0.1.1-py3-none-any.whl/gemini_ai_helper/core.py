import os
import google.generativeai as genai
from .utils import clean_text


api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY not set in environment")

genai.configure(api_key=api_key)

model = genai.GenerativeModel("gemini-1.5-flash")

def get_ai_response(prompt:str)->str:
        response=model.generate_content(prompt)

        return clean_text(response.text)

def summerize_text(text):
      prompt=text
      return get_ai_response(prompt)
