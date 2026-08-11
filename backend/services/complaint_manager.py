from sqlalchemy.orm import Session
from sqlalchemy import desc, or_
from datetime import datetime
from typing import List, Optional

from ..models import Complaint, StatusHistory, User
from ..schemas import ComplaintCreate
from .audit_service import AuditService

# --------------------------------------------------------------------------------
# COMPLAINT MANAGER
# This file contains all the "business logic" for complaints. 
# --------------------------------------------------------------------------------

class ComplaintManager:
    
    @staticmethod
    def create_complaint(db: Session, complaint_data: ComplaintCreate, ai_result: dict, citizen_id: str = None) -> Complaint:
        new_complaint = Complaint(
            description=complaint_data.description,
            location=complaint_data.location,
            citizen_contact=complaint_data.citizen_contact,
            citizen_id=citizen_id,
            category=ai_result.get("category", "Uncategorized"),
            priority=ai_result.get("priority", "Medium"),
            ai_summary=ai_result.get("summary", ""),
            ai_confidence=ai_result.get("confidence", 0.0),
            status="SUBMITTED"
        )
        
        db.add(new_complaint)
        db.commit()
        db.refresh(new_complaint)
        
        history_entry = StatusHistory(
            complaint_id=new_complaint.complaint_id,
            old_status="None",
            new_status="SUBMITTED",
            changed_by="System"
        )
        db.add(history_entry)
        db.commit()
        
        return new_complaint

    @staticmethod
    def get_complaint(db: Session, complaint_id: str) -> Optional[Complaint]:
        return db.query(Complaint).filter(Complaint.complaint_id == complaint_id).first()

    @staticmethod
    def list_complaints(db: Session, 
                        category: Optional[str] = None, 
                        priority: Optional[str] = None, 
                        status: Optional[str] = None,
                        department: Optional[str] = None,
                        assigned_to: Optional[str] = None,
                        citizen_id: Optional[str] = None) -> List[Complaint]:
        query = db.query(Complaint)
        if category:
            query = query.filter(Complaint.category == category)
        if priority:
            query = query.filter(Complaint.priority == priority)
        if status:
            query = query.filter(Complaint.status == status)
        if department:
            query = query.filter(Complaint.assigned_department == department)
        if assigned_to:
            query = query.filter(Complaint.assigned_to == assigned_to)
        if citizen_id:
            query = query.filter(Complaint.citizen_id == citizen_id)
            
        query = query.order_by(desc(Complaint.created_at))
        return query.all()

    @staticmethod
    def update_status(db: Session, complaint_id: str, new_status: str, changed_by_user: User, note: str = None) -> Optional[Complaint]:
        complaint = db.query(Complaint).filter(Complaint.complaint_id == complaint_id).first()
        if not complaint:
            return None
            
        old_status = complaint.status
        if old_status == new_status:
            return complaint
            
        complaint.status = new_status
        if new_status == "RESOLVED":
            complaint.resolved_at = datetime.utcnow()
        elif old_status == "RESOLVED" and new_status != "RESOLVED":
            complaint.resolved_at = None
            
        history_entry = StatusHistory(
            complaint_id=complaint.complaint_id,
            old_status=old_status,
            new_status=new_status,
            changed_by=changed_by_user.username
        )
        db.add(history_entry)
        
        AuditService.log_action(
            db, user=changed_by_user.username, role=changed_by_user.role, 
            action="Update Status", resource="Complaint", resource_id=complaint_id, 
            old_value=old_status, new_value=new_status
        )
        
        db.commit()
        db.refresh(complaint)
        return complaint

    @staticmethod
    def assign_complaint(db: Session, complaint_id: str, department: Optional[str], assigned_to: Optional[str], assigned_by_user: User) -> Optional[Complaint]:
        complaint = db.query(Complaint).filter(Complaint.complaint_id == complaint_id).first()
        if not complaint:
            return None
            
        if department:
            old_dept = complaint.assigned_department
            complaint.assigned_department = department
            if old_dept != department:
                AuditService.log_action(db, user=assigned_by_user.username, role=assigned_by_user.role, action="Reassign Department", resource="Complaint", resource_id=complaint_id, old_value=old_dept, new_value=department)
            
        if assigned_to:
            old_officer = complaint.assigned_to
            complaint.assigned_to = assigned_to
            if old_officer != assigned_to:
                AuditService.log_action(db, user=assigned_by_user.username, role=assigned_by_user.role, action="Assign Field Officer", resource="Complaint", resource_id=complaint_id, old_value=old_officer, new_value=assigned_to)

        if complaint.status in ["SUBMITTED", "AI_ANALYZED"]:
            # Auto update status when assigned
            complaint.status = "ASSIGNED"
            db.add(StatusHistory(complaint_id=complaint.complaint_id, old_status=complaint.status, new_status="ASSIGNED", changed_by=assigned_by_user.username))

        db.commit()
        db.refresh(complaint)
        return complaint
