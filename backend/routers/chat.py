from fastapi import APIRouter, Depends, HTTPException, status
from typing import Any
import os

from ..schemas import ChatRequest, ChatResponse
from ..services.ai_service import AIAnalyzer

router = APIRouter()

# Instantiate the AI Service just like we do in complaints.py
# We check if LLM_API_KEY is present to determine if we run in API mode.
use_llm_api = bool(os.getenv("LLM_API_KEY"))
ai_analyzer = AIAnalyzer(use_llm_api=use_llm_api)

@router.post("", response_model=ChatResponse)
def chat_with_bot(request: ChatRequest) -> Any:
    """
    Endpoint for the frontend chatbot widget.
    Takes a message and optional history, and returns the AI's response.
    """
    try:
        reply = ai_analyzer.chat_with_citizen(request.message, request.history)
        return {"reply": reply}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Chatbot failed to process message: {str(e)}"
        )
