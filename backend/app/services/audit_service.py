from typing import Optional
from sqlalchemy.orm import Session
from app.models import AuditLog

def log_action(db: Session, user_id: Optional[int], action: str, details: Optional[str] = None):
    try:
        log_entry = AuditLog(
            user_id=user_id,
            action=action,
            details=details
        )
        db.add(log_entry)
        db.commit()
        print(f"AUDIT LOG: User {user_id} - {action} - {details}")
    except Exception as e:
        db.rollback()
        print(f"Failed to write audit log: {e}")
