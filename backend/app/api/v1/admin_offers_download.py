from fastapi import APIRouter, Depends, HTTPException, Response
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession
from io import BytesIO

from app.api.deps import get_current_user
from app.core.database import get_db
from app.models.user import User
from app.repositories.offer_repository import OfferRepository
from app.services.storage_service import StorageService

router = APIRouter(prefix="/admin/offers", tags=["admin.offers"])


@router.get("/{offer_id}/download")
async def download_offer(offer_id: str, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    if user.role not in ("ADMIN", "MAIN_ADMIN"):
        raise HTTPException(status_code=403, detail="Forbidden")

    offer = await OfferRepository(db).get_by_id(offer_id)
    if not offer or not offer.offer_letter_storage_key:
        raise HTTPException(status_code=404, detail="Offer or file not found")

    storage = StorageService()
    try:
        data = storage.read(offer.offer_letter_storage_key)
    except Exception:
        raise HTTPException(status_code=404, detail="File not found")

    return StreamingResponse(BytesIO(data), media_type="application/pdf", headers={"Content-Disposition": f"attachment; filename=offer_{offer.id}.pdf"})
