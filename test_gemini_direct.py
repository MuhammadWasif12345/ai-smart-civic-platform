import os
import sys
from dotenv import load_dotenv

# Load the env variables explicitly for the test
load_dotenv("backend/.env")

# Add backend to path so imports work
sys.path.append(os.path.join(os.path.dirname(__file__), "backend"))
from services.ai_service import AIAnalyzer

analyzer = AIAnalyzer(use_llm_api=True)
try:
    result = analyzer._analyze_with_gemini("There is a massive pothole in front of the local high school that is causing cars to swerve dangerously.")
    print("SUCCESS!")
    print(result)
except Exception as e:
    print(f"FAILED WITH EXCEPTION: {e}")
