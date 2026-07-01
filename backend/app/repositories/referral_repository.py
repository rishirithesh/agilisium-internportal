import uuid

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.referral import Referral, ReferralStatus, ReferralTimelineEvent


class ReferralRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, referral: Referral) -> Referral:
        self.db.add(referral)
        await self.db.flush()
        await self.db.refresh(referral)
        return referral

    async def get_by_id(self, referral_id: uuid.UUID, with_timeline: bool = False) -> Referral | None:
        query = select(Referral).where(
            Referral.id == referral_id, Referral.deleted_at.is_(None)
        )
        if with_timeline:
            query = query.options(selectinload(Referral.timeline_events))
        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def list_for_employee(
        self, employee_id: uuid.UUID, page: int, page_size: int
    ) -> tuple[list[Referral], int]:
        base = select(Referral).where(
            Referral.referred_by_id == employee_id, Referral.deleted_at.is_(None)
        )
        return await self._paginate(base, page, page_size)

    async def list_all(
        self, page: int, page_size: int, status: ReferralStatus | None = None
    ) -> tuple[list[Referral], int]:
        base = select(Referral).where(Referral.deleted_at.is_(None))
        if status:
            base = base.where(Referral.status == status)
        return await self._paginate(base, page, page_size)

    async def _paginate(self, base_query, page: int, page_size: int) -> tuple[list[Referral], int]:
        count_result = await self.db.execute(
            select(func.count()).select_from(base_query.subquery())
        )
        total = count_result.scalar_one()

        result = await self.db.execute(
            base_query.order_by(Referral.created_at.desc())
            .offset((page - 1) * page_size)
            .limit(page_size)
        )
        items = list(result.scalars().all())
        return items, total

    async def add_timeline_event(self, event: ReferralTimelineEvent) -> ReferralTimelineEvent:
        self.db.add(event)
        await self.db.flush()
        return event

    async def get_active_by_email(self, email: str) -> Referral | None:
        from sqlalchemy import select

        # Active = not REJECTED and not COMPLETED
        from app.models.referral import ReferralStatus

        query = (
            select(Referral)
            .where(Referral.candidate_email == email, Referral.deleted_at.is_(None))
            .where(~Referral.status.in_([ReferralStatus.REJECTED, ReferralStatus.COMPLETED]))
        )
        result = await self.db.execute(query)
        return result.scalar_one_or_none()
