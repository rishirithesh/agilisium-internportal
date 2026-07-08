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
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
