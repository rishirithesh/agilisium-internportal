from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user
from app.core.database import get_db
from app.models.user import User
from app.services.offer_service import OfferService
from app.repositories.offer_repository import OfferRepository
from app.services.storage_service import StorageService
from fastapi.responses import StreamingResponse
from io import BytesIO
from typing import List
from pydantic import BaseModel
from sqlalchemy import select

router = APIRouter(prefix="/offers", tags=["offers"])


@router.post("/{offer_id}/accept")
async def accept_offer(offer_id: str, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    try:
        offer = await OfferService(db).accept_offer(offer_id=offer_id, user_id=user.id)
        return {"success": True, "offer_id": str(offer.id)}
    except Exception as exc:
        raise HTTPException(400, str(exc)) from exc


@router.get("/{offer_id}/download")
async def download_offer_intern(offer_id: str, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    # Interns and admins can download
    offer = await OfferRepository(db).get_by_id(offer_id)
    if not offer or not offer.offer_letter_storage_key:
        raise HTTPException(status_code=404, detail="Offer or file not found")

    # If not admin ensure user matches referral intern
    if user.role not in ("ADMIN", "MAIN_ADMIN"):
        from app.repositories.referral_repository import ReferralRepository

        referral = await ReferralRepository(db).get_by_id(offer.referral_id)
        if referral and referral.intern_user_id and str(referral.intern_user_id) != str(user.id):
            raise HTTPException(status_code=403, detail="Forbidden")

    storage = StorageService()
    try:
        data = storage.read(offer.offer_letter_storage_key)
    except Exception:
        raise HTTPException(status_code=404, detail="File not found")

    return StreamingResponse(BytesIO(data), media_type="application/pdf", headers={"Content-Disposition": f"attachment; filename=offer_{offer.id}.pdf"})


class OfferItem(BaseModel):
    id: str
    referral_id: str
    position_title: str
    status: str
    created_at: str | None


@router.get("", response_model=List[OfferItem])
async def list_my_offers(user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)) -> List[OfferItem]:
    # List offers associated with referrals where user is intern or referrer
    stmt = select(OfferRepository.__annotations__.get('Offer', None) or "offers").limit(0)
    # Fallback simple query
    result = await db.execute("SELECT id, referral_id, position_title, status, created_at FROM offers WHERE referral_id IN (SELECT id FROM referrals WHERE intern_user_id = :uid OR referred_by_id = :uid) ORDER BY created_at DESC", {"uid": str(user.id)})
    rows = result.fetchall()
    items = [OfferItem(id=str(r[0]), referral_id=str(r[1]), position_title=r[2], status=str(r[3]), created_at=r[4].isoformat() if r[4] else None) for r in rows]
    return items
