import os
import sys
from dotenv import load_dotenv

load_dotenv("backend/.env")
import google.generativeai as genai

api_key = os.getenv("LLM_API_KEY")
genai.configure(api_key=api_key)

try:
    model = genai.GenerativeModel('gemini-2.5-flash')
    response = model.generate_content("Testing 123")
    print("SUCCESS!")
    print(response.text)
except Exception as e:
    print(f"FAILED WITH EXCEPTION: {e}")
