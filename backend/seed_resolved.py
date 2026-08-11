import sys
import os
import random
from datetime import datetime, timedelta

from backend.database import SessionLocal
from backend.models import Complaint, StatusHistory

db = SessionLocal()

try:
    for i in range(5):
        # Create a resolved complaint
        created_at = datetime.utcnow() - timedelta(days=random.randint(2, 10))
        resolved_at = created_at + timedelta(hours=random.randint(2, 48))
        
        c_id = str(random.randint(101, 99999))
        
        complaint = Complaint(
            complaint_id=c_id,
            description=f"Automated seed issue #{i} for analytics",
            category="Roads & Infrastructure",
            priority="Medium",
            location="Downtown District",
            status="Resolved",
            created_at=created_at,
            resolved_at=resolved_at,
            assigned_department="Roads Department"
        )
        db.add(complaint)
        
        # Add status histories to make it look real
        hist1 = StatusHistory(complaint_id=c_id, old_status="Submitted", new_status="In Progress", changed_at=created_at + timedelta(hours=1), changed_by="System")
        hist2 = StatusHistory(complaint_id=c_id, old_status="In Progress", new_status="Resolved", changed_at=resolved_at, changed_by="Field Officer")
        db.add(hist1)
        db.add(hist2)

    db.commit()
    print("Successfully added 5 resolved complaints.")
except Exception as e:
    db.rollback()
    print(f"Error: {e}")
finally:
    db.close()
