import os
import sys
import json
import logging

# Add the parent directory to the path so we can import the backend modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from backend.services.ai_service import AIAnalyzer

# Setup basic logging to see the output
logging.basicConfig(level=logging.INFO, format='%(message)s')

def run_tests():
    """
    This script runs the 20 sample complaints through our AIAnalyzer to verify
    its performance. It checks if the predicted category and priority reasonably
    match our human expectations.
    """
    logging.info("==================================================")
    logging.info("   AI SMART CIVIC SERVICES - AI TESTING SCRIPT    ")
    logging.info("==================================================\n")
    
    # We force USE_LLM_API to true here for testing the Gemini integration,
    # as requested by the user, but this can be toggled to false to test HuggingFace.
    use_api = os.getenv("USE_LLM_API", "true").lower() == "true"
    logging.info(f"Mode: {'Gemini API' if use_api else 'Local HuggingFace Models'}")
    
    analyzer = AIAnalyzer(use_llm_api=use_api)
    
    # Load the 20 sample complaints
    sample_file_path = os.path.join(os.path.dirname(__file__), "sample_complaints.json")
    with open(sample_file_path, "r") as f:
        complaints = json.load(f)
        
    correct_category = 0
    correct_priority = 0
    total = len(complaints)
    
    for i, c in enumerate(complaints, 1):
        text = c["description"]
        expected_cat = c["expected_category"]
        expected_pri = c["expected_priority"] # This is a list of acceptable answers
        
        logging.info(f"--- Test {i}/{total} ---")
        logging.info(f"Text: '{text}'")
        
        # Run the AI!
        result = analyzer.analyze_complaint(text)
        
        predicted_cat = result["category"]
        predicted_pri = result["priority"]
        summary = result["summary"]
        
        # Check if the AI's answer matches our expectations
        cat_match = predicted_cat == expected_cat
        pri_match = predicted_pri in expected_pri
        
        if cat_match:
            correct_category += 1
        if pri_match:
            correct_priority += 1
            
        logging.info(f"Category:  {predicted_cat} (Expected: {expected_cat}) - {'✅' if cat_match else '❌'}")
        logging.info(f"Priority:  {predicted_pri} (Expected: {expected_pri}) - {'✅' if pri_match else '❌'}")
        logging.info(f"Summary:   {summary}\n")
        
    # Print the final score
    logging.info("==================================================")
    logging.info("                  FINAL RESULTS                   ")
    logging.info("==================================================")
    logging.info(f"Category Match Rate: {correct_category}/{total} ({round((correct_category/total)*100)}%)")
    logging.info(f"Priority Match Rate: {correct_priority}/{total} ({round((correct_priority/total)*100)}%)")
    logging.info("\nNote: 100% accuracy is not required or expected, especially for ambiguous text.")

if __name__ == "__main__":
    run_tests()
