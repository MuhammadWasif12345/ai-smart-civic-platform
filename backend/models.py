# We import the base classes needed to describe a database table using Python code
from sqlalchemy import Column, String, Text, Float, DateTime, ForeignKey
# We import relationship to link tables together (e.g., a Complaint has many StatusHistories)
from sqlalchemy.orm import relationship
import uuid
import random
from datetime import datetime

# We import the shared Base class we set up in database.py
from .database import Base

# --------------------------------------------------------------------------------
# COMPLAINT MODEL
# This table stores the actual civic complaints submitted by citizens.
# --------------------------------------------------------------------------------
class Complaint(Base):
    # This tells SQLAlchemy to name the table "complaints" in the database
    __tablename__ = "complaints"

    complaint_id = Column(String, primary_key=True, default=lambda: str(random.randint(101, 99999)))
    description = Column(Text, nullable=False)
    category = Column(String, default="Uncategorized")
    priority = Column(String, default="Medium")
    ai_summary = Column(Text, nullable=True)
    ai_confidence = Column(Float, nullable=True)
    location = Column(String, nullable=False)
    image_path = Column(String, nullable=True)
    
    # Status progression (Submitted, AI Analyzed, Pending Assignment, Assigned, In Progress, Resolved)
    status = Column(String, default="Submitted")
    
    assigned_department = Column(String, nullable=True)
    # The specific username of the Field Officer assigned to this complaint
    assigned_to = Column(String, nullable=True)
    
    citizen_id = Column(String, ForeignKey("users.id"), nullable=True)
    citizen_contact = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    resolved_at = Column(DateTime, nullable=True)

    history = relationship("StatusHistory", back_populates="complaint")


# --------------------------------------------------------------------------------
# STATUS HISTORY MODEL
# This table keeps an audit trail for STATUS changes specifically.
# --------------------------------------------------------------------------------
class StatusHistory(Base):
    __tablename__ = "status_history"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    complaint_id = Column(String, ForeignKey("complaints.complaint_id"))
    old_status = Column(String, nullable=False)
    new_status = Column(String, nullable=False)
    changed_at = Column(DateTime, default=datetime.utcnow)
    changed_by = Column(String, nullable=False) # Username of whoever changed it

    complaint = relationship("Complaint", back_populates="history")


# --------------------------------------------------------------------------------
# USER MODEL (Replaces old Admin model to support 5-Role RBAC)
# Roles: CITIZEN, FIELD_OFFICER, SUPERVISOR, MUNICIPAL_ADMIN, SUPER_ADMIN
# --------------------------------------------------------------------------------
class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    
    # RBAC Role
    role = Column(String, default="CITIZEN", nullable=False)
    
    # E.g., "Water Department". Useful for Field Officers and Supervisors.
    department = Column(String, nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)


# --------------------------------------------------------------------------------
# AUDIT LOG MODEL
# Generic audit log for privileged operations (assignments, logins, system changes)
# --------------------------------------------------------------------------------
class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    timestamp = Column(DateTime, default=datetime.utcnow)
    
    # Who performed the action
    user = Column(String, nullable=False)
    role = Column(String, nullable=False)
    
    # What did they do? (e.g., "Complaint Assignment", "Login")
    action = Column(String, nullable=False)
    
    # What was affected? (e.g., "Complaint", "System")
    resource = Column(String, nullable=True)
    resource_id = Column(String, nullable=True)
    
    # Details
    old_value = Column(String, nullable=True)
    new_value = Column(String, nullable=True)
