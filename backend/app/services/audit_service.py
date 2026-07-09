<<<<<<< HEAD
import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.audit_log import AuditLog


class AuditService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def log(
        self,
        *,
        actor_id: uuid.UUID | None,
        action: str,
        resource_type: str,
        resource_id: str | None = None,
        metadata: dict | None = None,
        ip_address: str | None = None,
    ) -> None:
        entry = AuditLog(
            actor_id=actor_id,
            action=action,
            resource_type=resource_type,
            resource_id=resource_id,
            metadata_json=metadata,
            ip_address=ip_address,
        )
        self.db.add(entry)
        await self.db.flush()
=======
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
>>>>>>> master
