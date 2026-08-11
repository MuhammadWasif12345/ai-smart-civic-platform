from sqlalchemy.orm import Session
from datetime import datetime
from ..models import AuditLog

class AuditService:
    @staticmethod
    def log_action(db: Session, user: str, role: str, action: str, resource: str = None, resource_id: str = None, old_value: str = None, new_value: str = None):
        log_entry = AuditLog(
            user=user,
            role=role,
            action=action,
            resource=resource,
            resource_id=resource_id,
            old_value=old_value,
            new_value=new_value,
            timestamp=datetime.utcnow()
        )
        db.add(log_entry)
        db.commit()
