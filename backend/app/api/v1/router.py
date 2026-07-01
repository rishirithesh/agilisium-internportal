from fastapi import APIRouter

from app.api.v1.auth import router as auth_router
from app.api.v1.notifications import router as notifications_router
from app.api.v1.referrals import router as referrals_router
from app.api.v1.admin_offers import router as admin_offers_router
from app.api.v1.offers import router as offers_router
from app.api.v1.admin_offers_download import router as admin_offers_download_router
from app.api.v1.admin_offers_versions import router as admin_offers_versions_router

api_router = APIRouter(prefix="/api/v1")
api_router.include_router(auth_router)
api_router.include_router(referrals_router)
api_router.include_router(notifications_router)
api_router.include_router(offers_router)
api_router.include_router(admin_offers_router)
api_router.include_router(admin_offers_download_router)
api_router.include_router(admin_offers_versions_router)
