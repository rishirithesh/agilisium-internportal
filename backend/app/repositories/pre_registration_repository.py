from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.pre_registration import PreRegistration


class PreRegistrationRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_email(self, email: str) -> PreRegistration | None:
        result = await self.db.execute(select(PreRegistration).where(PreRegistration.email == email))
        return result.scalar_one_or_none()

    async def create_or_update(self, record: PreRegistration) -> PreRegistration:
        existing = await self.get_by_email(record.email)
        if existing:
            # update in place
            existing.otp_hash = record.otp_hash
            existing.otp_expires_at = record.otp_expires_at
            existing.verified = record.verified
            existing.attempts = record.attempts
            await self.db.flush()
            return existing
        self.db.add(record)
        await self.db.flush()
        await self.db.refresh(record)
        return record

    async def delete(self, record: PreRegistration) -> None:
        await self.db.delete(record)
        await self.db.flush()
