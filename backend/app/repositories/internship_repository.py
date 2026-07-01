from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
import uuid

from app.models.internship import Internship


class InternshipRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, internship: Internship) -> Internship:
        self.db.add(internship)
        await self.db.flush()
        return internship

    async def get_by_user(self, user_id: uuid.UUID):
        result = await self.db.execute(select(Internship).where(Internship.user_id == user_id))
        return result.scalars().all()
