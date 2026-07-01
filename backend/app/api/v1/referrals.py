import uuid

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user
from app.core.database import get_db
from app.core.exceptions import AIRPException
from app.models.referral import ReferralStatus
from app.models.user import User
from app.schemas.referral import (
    PaginatedReferrals,
    ReferralCreateRequest,
    ReferralDetailResponse,
    ReferralResponse,
    ReferralTransitionRequest,
    InternRegistrationRequest,
)
from app.services.referral_service import ReferralService
from pydantic import BaseModel, Field

router = APIRouter(prefix="/referrals", tags=["referrals"])


@router.post("", response_model=ReferralResponse, status_code=201)
async def create_referral(
    payload: ReferralCreateRequest,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> ReferralResponse:
    try:
        referral = await ReferralService(db).create_referral(
            employee_id=user.id, role=user.role, payload=payload
        )
        return ReferralResponse.model_validate(referral)
    except AIRPException as exc:
        raise HTTPException(exc.status_code, exc.message) from exc


@router.get("", response_model=PaginatedReferrals)
async def list_referrals(
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
    status: ReferralStatus | None = None,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> PaginatedReferrals:
    items, total = await ReferralService(db).list_referrals(
        actor_id=user.id, role=user.role, page=page, page_size=page_size, status=status
    )
    return PaginatedReferrals(
        items=[ReferralResponse.model_validate(i) for i in items],
        total=total,
        page=page,
        page_size=page_size,
    )


@router.get("/{referral_id}", response_model=ReferralDetailResponse)
async def get_referral(
    referral_id: uuid.UUID,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> ReferralDetailResponse:
    try:
        referral = await ReferralService(db).get_referral(referral_id, actor_id=user.id, role=user.role)
        return ReferralDetailResponse.model_validate(referral)
    except AIRPException as exc:
        raise HTTPException(exc.status_code, exc.message) from exc


@router.post("/{referral_id}/transition", response_model=ReferralResponse)
async def transition_referral(
    referral_id: uuid.UUID,
    payload: ReferralTransitionRequest,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> ReferralResponse:
    try:
        referral = await ReferralService(db).transition_status(
            referral_id=referral_id,
            target_status=payload.target_status,
            actor_id=user.id,
            role=user.role,
            note=payload.note,
        )
        return ReferralResponse.model_validate(referral)
    except AIRPException as exc:
        raise HTTPException(exc.status_code, exc.message) from exc


@router.post("/{referral_id}/register", status_code=201)
async def register_referral_candidate(
    referral_id: uuid.UUID,
    payload: InternRegistrationRequest,
    db: AsyncSession = Depends(get_db),
) -> dict:
    try:
        pending = await ReferralService(db).register_intern(
            referral_id=referral_id,
            token=payload.token,
            email=payload.email,
            password=payload.password,
            entered_details=payload.entered_details or {},
        )
        return {"success": True, "message": "Registration received and pending employee approval"}
    except AIRPException as exc:
        raise HTTPException(exc.status_code, exc.message) from exc


@router.patch("/{referral_id}/approve", response_model=ReferralResponse)
async def approve_referral(
    referral_id: uuid.UUID,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> ReferralResponse:
    try:
        referral = await ReferralService(db).approve_pending_registration(
            referral_id=referral_id, actor_id=user.id, role=user.role
        )
        return ReferralResponse.model_validate(referral)
    except AIRPException as exc:
        raise HTTPException(exc.status_code, exc.message) from exc


class RejectRequest(BaseModel):
    reason: str = Field(min_length=20)


@router.patch("/{referral_id}/reject", response_model=ReferralResponse)
async def reject_referral(
    referral_id: uuid.UUID,
    payload: RejectRequest,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> ReferralResponse:
    try:
        referral = await ReferralService(db).reject_pending_registration(
            referral_id=referral_id, actor_id=user.id, role=user.role, reason=payload.reason
        )
        return ReferralResponse.model_validate(referral)
    except AIRPException as exc:
        raise HTTPException(exc.status_code, exc.message) from exc


@router.get("/{referral_id}/approve_by_token", response_model=ReferralResponse)
async def approve_by_token(referral_id: uuid.UUID, token: str = Query(...), db: AsyncSession = Depends(get_db)) -> ReferralResponse:
    referral = await ReferralService(db).referrals.get_by_id(referral_id)
    if not referral:
        raise HTTPException(status_code=404, detail="Referral not found")

    from app.core.security import verify_password
    from datetime import datetime, timezone
    from app.core.exceptions import AuthorizationError
    from app.core.permissions import Role

    if not referral.employee_action_token_hash or not referral.employee_action_expires_at:
        raise HTTPException(status_code=403, detail="Token not available")
    if datetime.now(timezone.utc) > referral.employee_action_expires_at:
        raise HTTPException(status_code=403, detail="Token expired")
    if not verify_password(token, referral.employee_action_token_hash):
        raise HTTPException(status_code=403, detail="Invalid token")

    try:
        approved = await ReferralService(db).approve_pending_registration(referral_id=referral.id, actor_id=referral.referred_by_id, role=Role.EMPLOYEE)
        # clear token
        referral.employee_action_token_hash = None
        await db.flush()
        return ReferralResponse.model_validate(approved)
    except AIRPException as exc:
        raise HTTPException(exc.status_code, exc.message) from exc


@router.get("/{referral_id}/reject_by_token")
async def reject_by_token(referral_id: uuid.UUID, token: str = Query(...), reason: str | None = Query(None), db: AsyncSession = Depends(get_db)):
    referral = await ReferralService(db).referrals.get_by_id(referral_id)
    if not referral:
        raise HTTPException(status_code=404, detail="Referral not found")

    from app.core.security import verify_password
    from datetime import datetime, timezone
    from app.core.permissions import Role

    if not referral.employee_action_token_hash or not referral.employee_action_expires_at:
        raise HTTPException(status_code=403, detail="Token not available")
    if datetime.now(timezone.utc) > referral.employee_action_expires_at:
        raise HTTPException(status_code=403, detail="Token expired")
    if not verify_password(token, referral.employee_action_token_hash):
        raise HTTPException(status_code=403, detail="Invalid token")

    if not reason:
        reason = "Rejected via email link"

    try:
        rejected = await ReferralService(db).reject_pending_registration(referral_id=referral.id, actor_id=referral.referred_by_id, role=Role.EMPLOYEE, reason=reason)
        referral.employee_action_token_hash = None
        await db.flush()
        return {"success": True, "referral_id": str(rejected.id)}
    except AIRPException as exc:
        raise HTTPException(exc.status_code, exc.message) from exc
