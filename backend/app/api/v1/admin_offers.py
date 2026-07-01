from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel

from app.api.deps import get_current_user
from app.core.database import get_db
from app.models.user import User
from app.services.offer_service import OfferService
from app.core.exceptions import AIRPException
from datetime import datetime
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.offer_repository import OfferRepository
from app.core.database import get_db
from typing import List


class OfferListItem(BaseModel):
    id: str
    referral_id: str
    position_title: str
    status: str
    created_at: str | None


@router.get("", response_model=List[OfferListItem])
async def list_offers_admin(user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    if user.role not in ("ADMIN", "MAIN_ADMIN"):
        raise HTTPException(status_code=403, detail="Forbidden")

    result = await db.execute("SELECT id, referral_id, position_title, status, created_at FROM offers ORDER BY created_at DESC LIMIT 200")
    rows = result.fetchall()
    items = [OfferListItem(id=str(r[0]), referral_id=str(r[1]), position_title=r[2], status=str(r[3]), created_at=r[4].isoformat() if r[4] else None) for r in rows]
    return items

router = APIRouter(prefix="/admin/offers", tags=["admin.offers"])


class UploadResponse(BaseModel):
    success: bool
    offer_id: str


@router.post("/upload", response_model=UploadResponse)
async def upload_offer(
    referral_id: str = Form(...),
    position_title: str = Form(None),
    stipend_amount: float | None = Form(None),
    file: UploadFile = File(...),
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> UploadResponse:
    # Only admins allowed
    if user.role not in ("ADMIN", "MAIN_ADMIN"):
        raise HTTPException(status_code=403, detail="Forbidden")

    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")

    contents = await file.read()
    # Validate PDF
    from app.utils.pdf_utils import validate_pdf
    ok, msg = validate_pdf(contents)
    if not ok:
        raise HTTPException(status_code=400, detail=msg)
    try:
        offer = await OfferService(db).upload_offer_letter(
            referral_id=referral_id,
            file_bytes=contents,
            original_name=file.filename,
            position_title=position_title,
            stipend_amount=stipend_amount,
            uploaded_by=user.id,
        )
        return UploadResponse(success=True, offer_id=str(offer.id))
    except AIRPException as exc:
        raise HTTPException(exc.status_code, exc.message) from exc
    except Exception as exc:
        raise HTTPException(500, str(exc)) from exc


@router.post("/{offer_id}/send", response_model=UploadResponse)
async def send_offer_endpoint(
    offer_id: str,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> UploadResponse:
    if user.role not in ("ADMIN", "MAIN_ADMIN"):
        raise HTTPException(status_code=403, detail="Forbidden")

    try:
        offer = await OfferService(db).send_offer(offer_id=offer_id, sent_by=user.id)
        return UploadResponse(success=True, offer_id=str(offer.id))
    except AIRPException as exc:
        raise HTTPException(exc.status_code, exc.message) from exc
    except Exception as exc:
        raise HTTPException(500, str(exc)) from exc
