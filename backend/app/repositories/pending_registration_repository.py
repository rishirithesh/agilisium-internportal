import uuid
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.pending_registration import PendingInternRegistration


class PendingRegistrationRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, record: PendingInternRegistration) -> PendingInternRegistration:
        self.db.add(record)
        await self.db.flush()
        await self.db.refresh(record)
        return record

    async def get_by_referral(self, referral_id: uuid.UUID) -> list[PendingInternRegistration]:
        result = await self.db.execute(select(PendingInternRegistration).where(PendingInternRegistration.referral_id == referral_id))
        return list(result.scalars().all())

    async def get_by_email(self, email: str) -> PendingInternRegistration | None:
        result = await self.db.execute(select(PendingInternRegistration).where(PendingInternRegistration.email == email))
        return result.scalar_one_or_none()

    async def delete(self, record: PendingInternRegistration) -> None:
        await self.db.delete(record)
        await self.db.flush()
