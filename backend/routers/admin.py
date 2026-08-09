from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional

from ..database import get_db
from ..schemas import PaginatedComplaints, ComplaintResponse, StatusUpdate, AssignDepartment
from ..services.complaint_manager import ComplaintManager
from ..services.notification_service import NotificationManager
from .auth import get_current_admin
from ..models import Admin

# --------------------------------------------------------------------------------
# ADMIN ROUTER
# These endpoints power the internal city dashboard. They allow staff to view all
# complaints, filter them, and update their statuses.
# Every endpoint here requires the user to be logged in (via `get_current_admin`).
# --------------------------------------------------------------------------------

# We add the `get_current_admin` dependency to the entire router, so we don't have
# to write it on every single function below.
router = APIRouter(dependencies=[Depends(get_current_admin)])

@router.get("/complaints", response_model=PaginatedComplaints)
def list_all_complaints(
    category: Optional[str] = Query(None, description="Filter by category"),
    priority: Optional[str] = Query(None, description="Filter by AI priority"),
    status: Optional[str] = Query(None, description="Filter by current status"),
    department: Optional[str] = Query(None, description="Filter by assigned department"),
    db: Session = Depends(get_db)
):
    """
    Fetch a list of complaints for the dashboard table.
    The admin can pass optional query parameters (like ?status=Open&priority=Critical)
    to filter the results.
    """
    complaints = ComplaintManager.list_complaints(
        db, category=category, priority=priority, status=status, department=department
    )
    
    # We wrap it in our Paginated schema so the frontend knows the total count
    return {"total": len(complaints), "complaints": complaints}


@router.patch("/complaints/{complaint_id}/status", response_model=ComplaintResponse)
def update_complaint_status(
    complaint_id: str, 
    update_data: StatusUpdate, 
    db: Session = Depends(get_db),
    admin: Admin = Depends(get_current_admin)  # We get the specific admin to log who did this
):
    """
    Change a complaint's status (e.g., from "Open" to "In Progress").
    """
    # We pass the admin's username so the database audit log knows who made the change
    updated_complaint = ComplaintManager.update_status(
        db, complaint_id, update_data.new_status, changed_by=admin.username
    )
    
    if not updated_complaint:
        raise HTTPException(status_code=404, detail="Complaint not found")
        
    # Attempt to notify the citizen about the change
    NotificationManager.notify_status_change(updated_complaint)
    
    return updated_complaint


@router.patch("/complaints/{complaint_id}/assign", response_model=ComplaintResponse)
def assign_complaint_department(
    complaint_id: str, 
    assign_data: AssignDepartment, 
    db: Session = Depends(get_db),
    admin: Admin = Depends(get_current_admin)
):
    """
    Assign a specific city department to handle the complaint.
    """
    updated_complaint = ComplaintManager.assign_department(
        db, complaint_id, assign_data.department, assigned_by=admin.username
    )
    
    if not updated_complaint:
        raise HTTPException(status_code=404, detail="Complaint not found")
        
    return updated_complaint
