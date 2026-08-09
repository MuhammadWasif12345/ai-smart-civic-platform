import os
import json
import logging
from typing import Dict, Any

# --------------------------------------------------------------------------------
# AI SERVICE
# This file is the brain of the operation. It takes a raw complaint from a citizen
# and figures out what category it is, how urgent it is, and summarizes it.
# --------------------------------------------------------------------------------

class AIAnalyzer:
    def __init__(self, use_llm_api: bool):
        # We store whether to use the external API (Google Gemini) or the local 
        # offline AI models (Hugging Face). This comes from the .env file.
        self.use_llm_api = use_llm_api
        
        # If we are using the local models, we load them now. We don't load them 
        # if we're using the API because local models take up a lot of RAM.
        if not self.use_llm_api:
            self._init_local_models()
        else:
            self._init_gemini_api()

    def _init_gemini_api(self):
        # Load environment variables so the API key is available
        from dotenv import load_dotenv
        env_path = os.path.join(os.path.dirname(__file__), "..", ".env")
        load_dotenv(env_path)

        # We import the new Google GenAI SDK only if we need it
        from google import genai
        
        # Grab the API key from our environment variables
        api_key = os.getenv("LLM_API_KEY")
        if not api_key:
            logging.warning("LLM_API_KEY is not set. Gemini API will fail.")
            
        # Initialize the new GenAI client
        self.gemini_client = genai.Client(api_key=api_key)

    def _init_local_models(self):
        # We import transformers and sumy here so they don't slow down startup 
        # if the user just wants the fast Gemini API.
        from transformers import pipeline
        from sumy.parsers.plaintext import PlaintextParser
        from sumy.nlp.tokenizers import Tokenizer
        from sumy.summarizers.lex_rank import LexRankSummarizer
        
        # Load a zero-shot classifier from Hugging Face. This model can categorize text 
        # into classes it hasn't explicitly been trained on, which is very flexible.
        # We use 'valhalla/distilbart-mnli-12-3' because it's smaller and faster than the default.
        logging.info("Loading local Hugging Face classifier... this may take a moment.")
        self.classifier = pipeline("zero-shot-classification", model="valhalla/distilbart-mnli-12-3")
        
        # Save the summarizer tools for later use
        self.Summarizer = LexRankSummarizer
        self.Parser = PlaintextParser
        self.Tokenizer = Tokenizer

    def analyze_complaint(self, text: str, image_base64: str = None) -> Dict[str, Any]:
        """
        The main entry point for this class. It hides the complexity of whether we 
        are using Gemini or local models. 
        Receives: The raw complaint text and an optional base64 encoded image.
        Returns: A dictionary with category, priority, summary, and confidence.
        """
        # If the text is empty or too short, we shouldn't waste AI resources on it
        if not text or len(text.strip()) < 10:
            return {
                "category": "Uncategorized",
                "priority": "Medium", 
                "summary": "Complaint text was too short for AI analysis.",
                "confidence": 0.0,
                "needs_review": True
            }

        if self.use_llm_api:
            return self._analyze_with_gemini(text, image_base64)
        else:
            # If we're local, we have to run three separate steps and combine them
            cat_result = self.classify_category(text)
            pri_result = self.predict_priority(text, cat_result["category"])
            summary = self.generate_summary(text)
            
            return {
                "category": cat_result["category"],
                "priority": pri_result["priority"],
                "summary": summary,
                "confidence": cat_result["confidence"],
                "needs_review": False
            }

    def _analyze_with_gemini(self, text: str, image_base64: str = None) -> Dict[str, Any]:
        """
        Sends the complaint to Google Gemini and asks for a strict JSON response.
        If an image is provided, it passes the image for multimodal analysis.
        """
        # We tell the AI exactly what format we want the answer in.
        prompt = f"""
        Analyze this civic complaint and provide a JSON response.
        Complaint: "{text}"
        
        Rules:
        1. "category" must be exactly one of: Road, Water/Drainage, Waste/Garbage, Electricity, Safety, Other.
        2. "priority" must be exactly one of: Low, Medium, High, Critical.
        3. "summary" must be a one-sentence actionable summary.
        4. "confidence" must be a float between 0.0 and 1.0 representing your certainty.
        
        Respond ONLY with a valid JSON object matching this schema:
        {{"category": "string", "priority": "string", "summary": "string", "confidence": 0.95}}
        """
        
        try:
            import base64
            from google import genai
            
            contents = [prompt]
            if image_base64:
                try:
                    image_bytes = base64.b64decode(image_base64)
                    image_part = genai.types.Part.from_bytes(data=image_bytes, mime_type="image/jpeg")
                    contents.append(image_part)
                except Exception as e:
                    logging.warning(f"Failed to process image payload: {e}")

            # Generate the content using Gemini
            response = self.gemini_client.models.generate_content(
                model='gemini-3.5-flash',
                contents=contents
            )
            
            # The AI sometimes wraps its JSON response in markdown blocks (```json ... ```).
            # We clean that up so the Python json.loads() function doesn't crash.
            response_text = response.text.replace("```json", "").replace("```", "").strip()
            
            # Parse the cleaned string into a Python dictionary
            result = json.loads(response_text)
            result["needs_review"] = False
            return result
            
        except Exception as e:
            # If Gemini times out, crashes, or gives us bad JSON, we don't want the app to die.
            # We log the error and return safe default values.
            logging.error(f"Gemini API Error: {str(e)}")
            return {
                "category": "Uncategorized",
                "priority": "Medium",
                "summary": "AI temporarily unavailable. Manual review required.",
                "confidence": 0.0,
                "needs_review": True
            }

    def classify_category(self, text: str) -> Dict[str, Any]:
        """
        Local AI method. Asks the Hugging Face model which category fits best.
        Limitation: Can struggle with vague slang or multi-issue complaints.
        """
        candidate_labels = ["Road", "Water/Drainage", "Waste/Garbage", "Electricity", "Safety", "Other"]
        
        try:
            # Send the text and the allowed labels to the Hugging Face pipeline
            result = self.classifier(text, candidate_labels)
            # The model returns them sorted by highest confidence first, so we grab index 0
            return {"category": result["labels"][0], "confidence": round(result["scores"][0], 2)}
        except Exception as e:
            logging.error(f"Local Classifier Error: {e}")
            return {"category": "Other", "confidence": 0.0}

    def predict_priority(self, text: str, category: str) -> Dict[str, str]:
        """
        Local AI method. Uses a rule-based dictionary of urgency words to guess priority.
        This is an 'explainable AI' heuristic, fulfilling the hackathon requirement
        for transparency when we aren't using the LLM API.
        """
        text_lower = text.lower()
        
        # If we see these words, it's an immediate emergency
        critical_keywords = ["fire", "spark", "accident", "blood", "collapsed", "trapped", "explosion"]
        # High urgency words
        high_keywords = ["danger", "leak", "huge", "broken", "stolen", "dark", "no water"]
        
        # Check against our lists
        if any(word in text_lower for word in critical_keywords):
            return {"priority": "Critical", "reasoning": "Detected critical emergency keywords."}
        elif any(word in text_lower for word in high_keywords):
            return {"priority": "High", "reasoning": "Detected high urgency keywords."}
        elif category in ["Electricity", "Water/Drainage"]:
             # Certain categories are naturally a bit higher priority
             return {"priority": "Medium", "reasoning": "Standard priority for utility issues."}
        else:
             return {"priority": "Low", "reasoning": "No urgent keywords detected."}

    def generate_summary(self, text: str) -> str:
        """
        Local AI method. Uses LexRank (via sumy) to extract the most important sentence.
        """
        try:
            # We parse the text into sentences
            parser = self.Parser.from_string(text, self.Tokenizer("english"))
            summarizer = self.Summarizer()
            
            # We ask the summarizer to give us the single most representative sentence
            summary_sentences = summarizer(parser.document, 1)
            
            if summary_sentences:
                return str(summary_sentences[0])
            else:
                # If it fails to summarize, just return the first 100 characters
                return text[:100] + "..."
        except Exception as e:
            logging.error(f"Local Summarizer Error: {e}")
            return text[:100] + "..."

    def chat_with_citizen(self, message: str, history: list) -> str:
        """
        Handles interactive chatbot conversations for citizens.
        Strictly restricted to answering questions related to the AI Smart Civic platform.
        """
        if not self.use_llm_api:
            return "I am currently running in offline mode. The AI Assistant requires an active internet connection and API key to chat with you."

        try:
            from google import genai
            
            # Format the conversation history for Gemini
            formatted_history = []
            for msg in history:
                # Map standard roles to Gemini roles
                gemini_role = "user" if msg.role == "user" else "model"
                formatted_history.append({"role": gemini_role, "parts": [{"text": msg.content}]})

            # Create a strict system prompt to keep the AI on track
            system_prompt = (
                "You are the AI Assistant for the 'AI Smart Civic Services' platform. "
                "Your job is to help citizens understand how to use the platform, report issues (like potholes, water leaks, etc.), "
                "and track their complaints. "
                "STRICT RULE: You MUST ONLY answer questions related to civic services, this platform, or reporting issues. "
                "If a user asks about anything else (programming, general knowledge, math, etc.), politely decline and say you can only help with civic matters. "
                "Keep your answers concise, friendly, and professional."
            )

            # Insert system prompt at the beginning (if no history, or emulate it)
            # Since Gemini GenAI API handles history directly, we can pass system instructions if supported by the model initialization,
            # or just prepend it to the first user message.
            if len(formatted_history) == 0:
                formatted_history.append({"role": "user", "parts": [{"text": f"System Instruction: {system_prompt}\n\nUser: {message}"}]})
            else:
                formatted_history.append({"role": "user", "parts": [{"text": message}]})

            response = self.gemini_client.models.generate_content(
                model='gemini-3.5-flash',
                contents=formatted_history
            )
            
            return response.text.strip()
            
        except Exception as e:
            logging.error(f"Chat API Error: {str(e)}")
            return "I'm sorry, I'm having trouble connecting to my brain right now. Please try again later."

