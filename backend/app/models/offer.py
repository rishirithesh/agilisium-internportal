import uuid
from datetime import date
from enum import StrEnum

from sqlalchemy import Date, Enum, ForeignKey, Numeric, String, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime

from app.models.base import AuditMixin, BaseEntity


class OfferStatus(StrEnum):
    DRAFT = "DRAFT"
    UPLOADED = "UPLOADED"
    SENT = "SENT"
    ACCEPTED = "ACCEPTED"
    DECLINED = "DECLINED"
    EXPIRED = "EXPIRED"


class Offer(BaseEntity, AuditMixin):
    __tablename__ = "offers"

    referral_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("referrals.id"), nullable=False, unique=True
    )
    position_title: Mapped[str] = mapped_column(String(255), nullable=False)
    stipend_amount: Mapped[float | None] = mapped_column(Numeric(10, 2), nullable=True)
    internship_start_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    internship_end_date: Mapped[date | None] = mapped_column(Date, nullable=True)

    status: Mapped[OfferStatus] = mapped_column(
        Enum(OfferStatus, name="offer_status"), nullable=False, default=OfferStatus.DRAFT
    )

    offer_letter_storage_key: Mapped[str | None] = mapped_column(String(1024), nullable=True)
    sent_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    accepted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    referral: Mapped["Referral"] = relationship(back_populates="offer")
    versions: Mapped[list["OfferVersion"]] = relationship(back_populates="offer", cascade="all, delete-orphan")
