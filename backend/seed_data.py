import os
import sys
import uuid
import random
from datetime import datetime, timedelta

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from backend.database import SessionLocal, Base, engine
from backend.models import Complaint, StatusHistory

def seed_db():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    
    # Force seed the 15 complaints

    sample_data = [
        {"desc": "There is a large water leak near the main road...", "cat": "Water/Drainage", "pri": "Critical", "sum": "Major water leak causing traffic issues."},
        {"desc": "Streetlight on Block C has been off for two weeks...", "cat": "Electricity", "pri": "Medium", "sum": "Streetlight out for two weeks in Block C."},
        {"desc": "Garbage bin outside the mosque has been overflowing...", "cat": "Waste/Garbage", "pri": "Medium", "sum": "Overflowing garbage bin near mosque."},
        {"desc": "Pothole on the main road near the school...", "cat": "Road", "pri": "High", "sum": "Dangerous pothole near school."},
        {"desc": "Sewage water is coming into our street after rain...", "cat": "Water/Drainage", "pri": "High", "sum": "Sewage water flooding street after rain."},
        {"desc": "Electricity pole near the park is leaning...", "cat": "Electricity", "pri": "Critical", "sum": "Leaning electricity pole poses fall risk."},
        {"desc": "No streetlights working on the entire lane...", "cat": "Electricity", "pri": "Medium", "sum": "Entire lane without working streetlights."},
        {"desc": "Open manhole near the bus stop...", "cat": "Safety", "pri": "Critical", "sum": "Dangerous open manhole near bus stop."},
        {"desc": "Trash collection truck hasn't come to our area...", "cat": "Waste/Garbage", "pri": "Medium", "sum": "Missed trash collection for over a week."},
        {"desc": "Water pipe burst outside house #45...", "cat": "Water/Drainage", "pri": "Critical", "sum": "Burst water pipe running for two days."},
        {"desc": "Speed breaker needed near the school gate...", "cat": "Road", "pri": "Low", "sum": "Request for speed breaker near school."},
        {"desc": "Broken drain cover on the footpath...", "cat": "Safety", "pri": "High", "sum": "Broken drain cover poses tripping hazard."},
        {"desc": "Illegal dumping of construction waste...", "cat": "Waste/Garbage", "pri": "Low", "sum": "Illegal construction waste dumping."},
        {"desc": "Transformer near the market making loud buzzing...", "cat": "Electricity", "pri": "Critical", "sum": "Sparking and buzzing transformer near market."},
        {"desc": "Road markings have completely faded...", "cat": "Road", "pri": "Low", "sum": "Faded road markings causing intersection confusion."},
    ]

    for item in sample_data:
        # random status: Open, Assigned, In Progress, Resolved
        status = random.choice(["Open", "Assigned", "In Progress", "Resolved"])
        c = Complaint(
            complaint_id=str(uuid.uuid4()),
            description=item["desc"],
            category=item["cat"],
            priority=item["pri"],
            ai_summary=item["sum"],
            ai_confidence=random.uniform(0.7, 0.99),
            location="City Area",
            status=status
        )
        # Random dates in the last 30 days
        days_ago = random.randint(1, 30)
        c.created_at = datetime.utcnow() - timedelta(days=days_ago)
        if status == "Resolved":
            c.resolved_at = c.created_at + timedelta(hours=random.randint(2, 72))
            
        db.add(c)
        db.commit()
        db.refresh(c)
        
        # Add a status history entry
        sh = StatusHistory(
            complaint_id=c.complaint_id,
            old_status="Open",
            new_status=status,
            changed_by="system"
        )
        db.add(sh)
    
    db.commit()
    db.close()
    print("Seeded database with 15 complaints!")

if __name__ == "__main__":
    seed_db()
