import uuid
from enum import StrEnum

from sqlalchemy import Enum, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import DateTime

from app.models.base import AuditMixin, BaseEntity
from datetime import datetime


class ReferralStatus(StrEnum):
    REFERRED = "REFERRED"
    INTERN_REGISTERED = "INTERN_REGISTERED"
    EMPLOYEE_APPROVED = "EMPLOYEE_APPROVED"
    PROFILE_SUBMITTED = "PROFILE_SUBMITTED"
    ADMIN_REVIEW = "ADMIN_REVIEW"
    CHANGES_REQUESTED = "CHANGES_REQUESTED"
    OFFER_GENERATED = "OFFER_GENERATED"
    OFFER_UPLOADED = "OFFER_UPLOADED"
    OFFER_SENT = "OFFER_SENT"
    OFFER_ACCEPTED = "OFFER_ACCEPTED"
    COMPLETED = "COMPLETED"
    REJECTED = "REJECTED"


class Referral(BaseEntity, AuditMixin):
    __tablename__ = "referrals"

    referred_by_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True
    )
    candidate_full_name: Mapped[str] = mapped_column(String(255), nullable=False)
    candidate_email: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    candidate_phone: Mapped[str | None] = mapped_column(String(32), nullable=True)
    position_applied: Mapped[str] = mapped_column(String(255), nullable=False)
    relationship_to_candidate: Mapped[str | None] = mapped_column(String(255), nullable=True)
    referral_notes: Mapped[str | None] = mapped_column(Text, nullable=True)

    status: Mapped[ReferralStatus] = mapped_column(
        Enum(ReferralStatus, name="referral_status"),
        nullable=False,
        default=ReferralStatus.REFERRED,
        index=True,
    )

    intern_user_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id"), nullable=True
    )

    intern_profile: Mapped["InternProfile | None"] = relationship(
        back_populates="referral", uselist=False, cascade="all, delete-orphan"
    )
    offer: Mapped["Offer | None"] = relationship(
        back_populates="referral", uselist=False, cascade="all, delete-orphan"
    )
    timeline_events: Mapped[list["ReferralTimelineEvent"]] = relationship(
        back_populates="referral", cascade="all, delete-orphan", order_by="ReferralTimelineEvent.created_at"
    )

    # Invitation token hash and expiry used for secure referral invitations
    invitation_token_hash: Mapped[str | None] = mapped_column(String(255), nullable=True)
    invitation_expires_at: Mapped[DateTime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    employee_approved_at: Mapped[DateTime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    # Token for employee one-tap approval/rejection links
    employee_action_token_hash: Mapped[str | None] = mapped_column(String(255), nullable=True)
    employee_action_expires_at: Mapped[DateTime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    offer_sent_at: Mapped[DateTime | None] = mapped_column(DateTime(timezone=True), nullable=True)


class ReferralTimelineEvent(BaseEntity):
    """Immutable append-only log of every status transition for a referral."""

    __tablename__ = "referral_timeline_events"

    referral_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("referrals.id"), nullable=False, index=True
    )
    from_status: Mapped[ReferralStatus | None] = mapped_column(
        Enum(ReferralStatus, name="referral_status"), nullable=True
    )
    to_status: Mapped[ReferralStatus] = mapped_column(
        Enum(ReferralStatus, name="referral_status"), nullable=False
    )
    actor_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id"), nullable=True
    )
    note: Mapped[str | None] = mapped_column(Text, nullable=True)

    referral: Mapped["Referral"] = relationship(back_populates="timeline_events")
