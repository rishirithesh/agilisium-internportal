import uuid

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user
from app.core.database import get_db
from app.core.exceptions import AIRPException
from app.models.user import User
from app.schemas.notification import PaginatedNotifications, NotificationResponse
from app.services.notification_service import NotificationService

router = APIRouter(prefix="/notifications", tags=["notifications"])


@router.get("", response_model=PaginatedNotifications)
async def list_notifications(
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> PaginatedNotifications:
    try:
        items, total = await NotificationService(db).list_for_user(user.id, page=page, page_size=page_size)
        return PaginatedNotifications(items=[NotificationResponse.model_validate(i) for i in items], total=total, page=page, page_size=page_size)
    except AIRPException as exc:
        raise HTTPException(exc.status_code, exc.message) from exc


@router.post("/{notification_id}/read", response_model=NotificationResponse)
async def mark_notification_read(
    notification_id: uuid.UUID,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> NotificationResponse:
    try:
        notification = await NotificationService(db).mark_read(notification_id=notification_id, user_id=user.id)
        return NotificationResponse.model_validate(notification)
    except AIRPException as exc:
        raise HTTPException(exc.status_code, exc.message) from exc


@router.post("/mark-all-read", response_model=dict)
async def mark_all_read(
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> dict:
    try:
        count = await NotificationService(db).mark_all_read(user.id)
        return {"updated": count}
    except AIRPException as exc:
        raise HTTPException(exc.status_code, exc.message) from exc
