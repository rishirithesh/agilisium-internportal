from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user
from app.core.database import get_db
from app.models.user import User
from app.repositories.offer_repository import OfferRepository
from app.models.offer_version import OfferVersion
from sqlalchemy import select

router = APIRouter(prefix="/admin/offers", tags=["admin.offers"])


@router.get("/{offer_id}/versions")
async def list_versions(offer_id: str, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    if user.role not in ("ADMIN", "MAIN_ADMIN"):
        raise HTTPException(status_code=403, detail="Forbidden")

    result = await db.execute(select(OfferVersion).where(OfferVersion.offer_id == offer_id).order_by(OfferVersion.uploaded_at.desc()))
    versions = result.scalars().all()
    return [{"id": str(v.id), "storage_key": v.storage_key, "uploaded_at": v.uploaded_at.isoformat()} for v in versions]
