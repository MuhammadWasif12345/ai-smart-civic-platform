from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from ..database import get_db
from ..schemas import ComplaintCreate, ComplaintResponse
from ..services.complaint_manager import ComplaintManager
from ..services.ai_service import AIAnalyzer
from .auth import get_current_user, require_role
from ..models import User
import os

# --------------------------------------------------------------------------------
# COMPLAINTS ROUTER (CITIZEN FACING)
# These endpoints are used by the public (citizens) to submit and track their issues.
# No login is required to access these.
# --------------------------------------------------------------------------------

router = APIRouter()

# Read from .env whether we're using Gemini API or local AI models
USE_LLM_API = os.getenv("USE_LLM_API", "true").lower() == "true"

# We instantiate the AI Analyzer once here so it doesn't have to reload 
# its heavy models on every single web request.
ai_analyzer = AIAnalyzer(use_llm_api=USE_LLM_API)

@router.post("", response_model=ComplaintResponse, status_code=status.HTTP_201_CREATED)
def submit_complaint(complaint: ComplaintCreate, db: Session = Depends(get_db)):
    """
    A citizen submits a new complaint.
    We immediately run it through the AI to categorize and prioritize it,
    then save the result to the database.
    """
    try:
        # Step 1: Send the citizen's text (and optional image) to our AI brain
        ai_result = ai_analyzer.analyze_complaint(complaint.description, complaint.image_base64)
        
        # Step 2: Save the complaint in the database along with the AI's findings
        new_complaint = ComplaintManager.create_complaint(db, complaint, ai_result)
        
        # We don't automatically set citizen_id here because this endpoint is public.
        # But if we were securely passing tokens to the submit endpoint, we could.
        # For this demo, citizens submit publicly and then track by ID. 
        # But for the dashboard "My Complaints" to work, we'll need an endpoint.
        
        # Step 3: Return the saved data (including the new complaint_id) back to the citizen
        return new_complaint
    except Exception as e:
        # If the database fails or something unexpected crashes, we catch it here.
        # We don't want to show the raw stack trace to the user, so we return a friendly 500 error.
        raise HTTPException(
            status_code=500,
            detail="Something went wrong on our end — please try again shortly."
        )

@router.get("/{complaint_id}", response_model=ComplaintResponse)
def track_complaint(complaint_id: str, db: Session = Depends(get_db)):
    """
    A citizen wants to check the status of a complaint they submitted previously.
    """
    # Look up the complaint in the database by its ID
    complaint = ComplaintManager.get_complaint(db, complaint_id)
    
    # If we couldn't find it, it means the citizen typed the ID wrong (or it was deleted)
    if not complaint:
        raise HTTPException(
            status_code=404,
            detail="We couldn't find a complaint with that ID — double-check and try again."
        )
        
    return complaint

@router.get("/my/list", response_model=list[ComplaintResponse], dependencies=[Depends(require_role(["CITIZEN"]))])
def get_my_complaints(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    """
    Returns only the complaints belonging to the logged-in citizen.
    """
    complaints = ComplaintManager.list_complaints(db, citizen_id=user.id)
    return complaints
