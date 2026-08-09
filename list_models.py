import os
import sys
from dotenv import load_dotenv

load_dotenv("backend/.env")
api_key = os.getenv("LLM_API_KEY")

import google.generativeai as genai
genai.configure(api_key=api_key)

for m in genai.list_models():
    if 'generateContent' in m.supported_generation_methods:
        print(m.name)
