from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional, List

from ..database import get_db
from ..schemas import PaginatedComplaints, ComplaintResponse, StatusUpdate, AssignComplaint, UserResponse, AuditLogResponse
from ..services.complaint_manager import ComplaintManager
from ..services.notification_service import NotificationManager
from .auth import get_current_user, require_role
from ..models import User, AuditLog

# --------------------------------------------------------------------------------
# ADMIN ROUTER
# Role-based API endpoints for staff.
# --------------------------------------------------------------------------------

router = APIRouter(dependencies=[Depends(get_current_user)])

@router.get("/me", response_model=UserResponse)
def get_my_profile(user: User = Depends(get_current_user)):
    return user

@router.get("/users", response_model=List[UserResponse], dependencies=[Depends(require_role(["SUPER_ADMIN", "MUNICIPAL_ADMIN", "SUPERVISOR"]))])
def get_users(role: Optional[str] = Query(None, description="Filter by role"), db: Session = Depends(get_db)):
    query = db.query(User)
    if role:
        query = query.filter(User.role == role)
    return query.all()

@router.get("/complaints", response_model=PaginatedComplaints, dependencies=[Depends(require_role(["SUPER_ADMIN", "MUNICIPAL_ADMIN", "SUPERVISOR", "FIELD_OFFICER"]))])
def list_all_complaints(
    category: Optional[str] = Query(None, description="Filter by category"),
    priority: Optional[str] = Query(None, description="Filter by AI priority"),
    status: Optional[str] = Query(None, description="Filter by current status"),
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    department = None
    assigned_to = None
    
    # Enforce RBAC filtering
    if user.role == "FIELD_OFFICER":
        assigned_to = user.username # Only see their own work
    elif user.role == "SUPERVISOR" and user.department:
        department = user.department # Only see their department's work
        
    complaints = ComplaintManager.list_complaints(
        db, category=category, priority=priority, status=status, 
        department=department, assigned_to=assigned_to
    )
    
    return {"total": len(complaints), "complaints": complaints}


@router.patch("/complaints/{complaint_id}/status", response_model=ComplaintResponse, dependencies=[Depends(require_role(["FIELD_OFFICER", "SUPERVISOR", "MUNICIPAL_ADMIN", "SUPER_ADMIN"]))])
def update_complaint_status(
    complaint_id: str, 
    update_data: StatusUpdate, 
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    updated_complaint = ComplaintManager.update_status(
        db, complaint_id, update_data.new_status, changed_by_user=user, note=update_data.note
    )
    
    if not updated_complaint:
        raise HTTPException(status_code=404, detail="Complaint not found")
        
    # NotificationManager.notify_status_change(updated_complaint)
    
    return updated_complaint


@router.patch("/complaints/{complaint_id}/assign", response_model=ComplaintResponse, dependencies=[Depends(require_role(["SUPERVISOR", "MUNICIPAL_ADMIN", "SUPER_ADMIN"]))])
def assign_complaint(
    complaint_id: str, 
    assign_data: AssignComplaint, 
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    updated_complaint = ComplaintManager.assign_complaint(
        db, complaint_id, assign_data.department, assign_data.assigned_to, assigned_by_user=user
    )
    
    if not updated_complaint:
        raise HTTPException(status_code=404, detail="Complaint not found")
        
    return updated_complaint


@router.patch("/complaints/{complaint_id}/field-update", response_model=ComplaintResponse, dependencies=[Depends(require_role(["FIELD_OFFICER"]))])
def field_update(
    complaint_id: str, 
    update_data: StatusUpdate, 
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    """
    Specific endpoint for field officers to provide updates.
    """
    updated_complaint = ComplaintManager.update_status(
        db, complaint_id, update_data.new_status, changed_by_user=user, note=update_data.note
    )
    
    if not updated_complaint:
        raise HTTPException(status_code=404, detail="Complaint not found")
        
    return updated_complaint


@router.get("/audit-logs", response_model=List[AuditLogResponse], dependencies=[Depends(require_role(["SUPER_ADMIN"]))])
def get_audit_logs(db: Session = Depends(get_db)):
    """
    Super Admin only: View system audit logs.
    """
    return db.query(AuditLog).order_by(AuditLog.timestamp.desc()).all()
