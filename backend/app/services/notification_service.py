import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import NotFoundError
from app.models.audit_log import Notification, NotificationType


class NotificationService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(
        self,
        *,
        user_id: uuid.UUID,
        type_: NotificationType,
        title: str,
        body: str | None = None,
        link_url: str | None = None,
    ) -> Notification:
        notification = Notification(
            user_id=user_id, type=type_, title=title, body=body, link_url=link_url
        )
        self.db.add(notification)
        await self.db.flush()
        return notification

    async def list_for_user(self, user_id: uuid.UUID, *, page: int, page_size: int) -> tuple[list[Notification], int]:
        stmt = (
            select(Notification)
            .where(Notification.user_id == user_id)
            .order_by(Notification.created_at.desc())
        )
        total_result = await self.db.execute(select(Notification.id).where(Notification.user_id == user_id))
        total = len(total_result.scalars().all())
        result = await self.db.execute(stmt.offset((page - 1) * page_size).limit(page_size))
        return list(result.scalars().all()), total

    async def mark_read(self, *, notification_id: uuid.UUID, user_id: uuid.UUID) -> Notification:
        result = await self.db.execute(
            select(Notification).where(Notification.id == notification_id, Notification.user_id == user_id)
        )
        notification = result.scalar_one_or_none()
        if not notification:
            raise NotFoundError("Notification not found")
        notification.is_read = True
        await self.db.flush()
        return notification

    async def mark_all_read(self, user_id: uuid.UUID) -> int:
        result = await self.db.execute(
            select(Notification).where(Notification.user_id == user_id, Notification.is_read.is_(False))
        )
        notifications = result.scalars().all()
        for notification in notifications:
            notification.is_read = True
        await self.db.flush()
        return len(notifications)
