import os
import sys
import uuid
import random
from datetime import datetime, timedelta

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from backend.database import SessionLocal, Base, engine
from backend.models import Complaint, StatusHistory, User, AuditLog
from backend.services.auth_service import AuthService

def seed_db():
    print("Dropping existing tables to apply new RBAC schema...")
    Base.metadata.drop_all(bind=engine)
    print("Creating new tables...")
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    
    # 1. SEED 5 ROLES
    print("Seeding RBAC Users...")
    users = [
        {"username": "citizen", "role": "CITIZEN", "department": None},
        {"username": "field", "role": "FIELD_OFFICER", "department": "Water/Drainage"},
        {"username": "supervisor", "role": "SUPERVISOR", "department": "Water/Drainage"},
        {"username": "municipal", "role": "MUNICIPAL_ADMIN", "department": None},
        {"username": "admin", "role": "SUPER_ADMIN", "department": None},
    ]
    
    default_password = os.getenv("ADMIN_PASSWORD", "admin123")
    hashed_pw = AuthService.get_password_hash(default_password)
    
    for u in users:
        new_user = User(
            username=u["username"],
            hashed_password=hashed_pw,
            role=u["role"],
            department=u["department"]
        )
        db.add(new_user)
    db.commit()
    
    citizen_user = db.query(User).filter(User.username == "citizen").first()

    # 2. SEED COMPLAINTS
    print("Seeding Complaints...")
    sample_data = [
        {"desc": "There is a large water leak near the main road...", "cat": "Water/Drainage", "pri": "Critical", "sum": "Major water leak causing traffic issues."},
        {"desc": "Streetlight on Block C has been off for two weeks...", "cat": "Electricity", "pri": "Medium", "sum": "Streetlight out for two weeks in Block C."},
        {"desc": "Garbage bin outside the mosque has been overflowing...", "cat": "Waste/Garbage", "pri": "Medium", "sum": "Overflowing garbage bin near mosque."},
        {"desc": "Pothole on the main road near the school...", "cat": "Road", "pri": "High", "sum": "Dangerous pothole near school."},
        {"desc": "Sewage water is coming into our street after rain...", "cat": "Water/Drainage", "pri": "High", "sum": "Sewage water flooding street after rain."},
        {"desc": "Electricity pole near the park is leaning...", "cat": "Electricity", "pri": "Critical", "sum": "Leaning electricity pole poses fall risk."},
        {"desc": "Broken drain cover on the footpath...", "cat": "Safety", "pri": "High", "sum": "Broken drain cover poses tripping hazard."},
        {"desc": "Illegal dumping of construction waste...", "cat": "Waste/Garbage", "pri": "Low", "sum": "Illegal construction waste dumping."},
        {"desc": "Transformer near the market making loud buzzing...", "cat": "Electricity", "pri": "Critical", "sum": "Sparking and buzzing transformer near market."},
        {"desc": "Road markings have completely faded...", "cat": "Road", "pri": "Low", "sum": "Faded road markings causing intersection confusion."},
    ]

    for i, item in enumerate(sample_data):
        # We need a proper workflow distribution:
        # SUBMITTED -> AI_ANALYZED -> ASSIGNED -> IN_PROGRESS -> RESOLVED
        status_options = ["SUBMITTED", "AI_ANALYZED", "ASSIGNED", "IN_PROGRESS", "RESOLVED"]
        status = random.choice(status_options)
        
        c = Complaint(
            complaint_id=str(uuid.uuid4()),
            description=item["desc"],
            category=item["cat"],
            priority=item["pri"],
            ai_summary=item["sum"],
            ai_confidence=random.uniform(0.7, 0.99),
            location="City Area",
            status=status,
            citizen_id=citizen_user.id if citizen_user else None
        )
        
        # If assigned or beyond, set department and officer
        if status in ["ASSIGNED", "IN_PROGRESS", "RESOLVED"]:
            c.assigned_department = item["cat"]
            # Assign some specifically to our Field Officer for demo purposes
            if item["cat"] == "Water/Drainage":
                c.assigned_to = "field"

        # Random dates in the last 30 days
        days_ago = random.randint(1, 30)
        c.created_at = datetime.utcnow() - timedelta(days=days_ago)
        if status == "RESOLVED":
            c.resolved_at = c.created_at + timedelta(hours=random.randint(2, 72))
            
        db.add(c)
        db.commit()
        db.refresh(c)
        
        # Add a status history entry
        sh = StatusHistory(
            complaint_id=c.complaint_id,
            old_status="SUBMITTED",
            new_status=status,
            changed_by="system"
        )
        db.add(sh)
    
    db.commit()
    db.close()
    print("Database seeded successfully with RBAC roles and realistic workflow data!")

if __name__ == "__main__":
    seed_db()
