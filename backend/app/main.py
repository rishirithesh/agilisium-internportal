<<<<<<< HEAD
import logging

from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.api.v1.router import api_router
from app.core.config import settings
from app.core.exceptions import AIRPException

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("airp")

app = FastAPI(
    title="AIRP - Agilisium Intern Referral Portal",
    version="1.0.0",
    description="Enterprise referral, onboarding, and offer-management platform.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
=======
import os
from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.core.config import settings
from app.api import auth, intern, employee, admin, super_admin

app = FastAPI(
    title="Agilisium Intern & Referral Portal (AIRP)",
    version="1.0"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
>>>>>>> master
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

<<<<<<< HEAD

@app.middleware("http")
async def security_headers_middleware(request: Request, call_next):
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    if settings.ENVIRONMENT != "local":
        response.headers["Strict-Transport-Security"] = "max-age=63072000; includeSubDomains"
        response.headers["Content-Security-Policy"] = "default-src 'self'"
    return response


@app.exception_handler(AIRPException)
async def airp_exception_handler(request: Request, exc: AIRPException) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content={"error_code": exc.error_code, "message": exc.message},
    )


@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    logger.exception("Unhandled exception on %s %s", request.method, request.url.path)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"error_code": "INTERNAL_ERROR", "message": "An unexpected error occurred"},
    )


@app.get("/health", tags=["health"])
async def health() -> dict:
    return {"status": "ok", "environment": settings.ENVIRONMENT}


app.include_router(api_router)
=======
# Ensure uploads directories exist (for local dev fallback)
os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
os.makedirs(os.path.join(settings.UPLOAD_DIR, "resumes"), exist_ok=True)
os.makedirs(os.path.join(settings.UPLOAD_DIR, "offers"), exist_ok=True)
os.makedirs(os.path.join(settings.UPLOAD_DIR, "presentations"), exist_ok=True)

# Mount uploads directory as static (local dev only; production files served from Supabase Storage URLs)
app.mount("/uploads", StaticFiles(directory=settings.UPLOAD_DIR), name="uploads")

# Include routers
api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(intern.router, prefix="/intern", tags=["intern"])
api_router.include_router(employee.router, prefix="/employee", tags=["employee"])
api_router.include_router(admin.router, prefix="/admin", tags=["admin"])
api_router.include_router(super_admin.router, prefix="/super-admin", tags=["super-admin"])

app.include_router(api_router, prefix="/api/v1")

# Route to download the official presentation template
@app.get("/api/v1/download/template")
def download_template():
    # Template is at the workspace root
    template_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "Remote Internship - Agilisium Template.pptx")
    if os.path.exists(template_path):
        return FileResponse(
            path=template_path,
            filename="Remote Internship - Agilisium Template.pptx",
            media_type="application/vnd.openxmlformats-officedocument.presentationml.presentation"
        )
    return {"error": "Template file not found"}

@app.get("/")
def read_root():
    return {"message": "Welcome to Agilisium Intern & Referral Portal (AIRP) API"}
>>>>>>> master
