import uuid
from datetime import datetime

from pydantic import BaseModel, EmailStr, Field

from app.models.referral import ReferralStatus


class ReferralCreateRequest(BaseModel):
    candidate_full_name: str = Field(min_length=2, max_length=255)
    candidate_email: EmailStr
    candidate_phone: str | None = Field(default=None, max_length=32)
    position_applied: str = Field(min_length=2, max_length=255)
    relationship_to_candidate: str | None = None
    referral_notes: str | None = None


class ReferralTransitionRequest(BaseModel):
    target_status: ReferralStatus
    note: str | None = None


class InternRegistrationRequest(BaseModel):
    token: str
    email: EmailStr
    password: str = Field(min_length=8)
    entered_details: dict | None = None


class TimelineEventResponse(BaseModel):
    id: uuid.UUID
    from_status: ReferralStatus | None
    to_status: ReferralStatus
    actor_id: uuid.UUID | None
    note: str | None
    created_at: datetime

    model_config = {"from_attributes": True}


class ReferralResponse(BaseModel):
    id: uuid.UUID
    referred_by_id: uuid.UUID
    candidate_full_name: str
    candidate_email: EmailStr
    candidate_phone: str | None
    position_applied: str
    relationship_to_candidate: str | None
    referral_notes: str | None
    status: ReferralStatus
    intern_user_id: uuid.UUID | None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class ReferralDetailResponse(ReferralResponse):
    timeline_events: list[TimelineEventResponse] = []


class PaginatedReferrals(BaseModel):
    items: list[ReferralResponse]
    total: int
    page: int
    page_size: int
