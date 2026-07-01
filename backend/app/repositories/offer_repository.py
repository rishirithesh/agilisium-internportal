import uuid
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.offer import Offer


class OfferRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, offer_id: uuid.UUID) -> Offer | None:
        result = await self.db.execute(select(Offer).where(Offer.id == offer_id))
        return result.scalar_one_or_none()

    async def create(self, offer: Offer):
        self.db.add(offer)
        await self.db.flush()
        return offer
