import os
import uuid
from datetime import date, datetime
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, BackgroundTasks, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_password_hash
from app.api.deps import get_current_active_user, RoleChecker
from app.models import User, Internship, Attendance, Project, CompanyProject
from app.schemas import InternshipResponse, UserResponse, ProjectResponse, AttendanceResponse
from app.services.email_service import send_email_background
from app.services.audit_service import log_action
from app.core.config import settings
from app.core.supabase_client import supabase

router = APIRouter()

# Max file size: 5MB
MAX_FILE_SIZE = 5 * 1024 * 1024

def validate_file(file: UploadFile, allowed_extensions: list[str]):
    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in allowed_extensions:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid file type. Allowed extensions: {', '.join(allowed_extensions)}"
        )
    # Check size
    file.file.seek(0, os.SEEK_END)
    size = file.file.tell()
    file.file.seek(0)
    if size > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File size exceeds the 5MB limit."
        )

def upload_to_supabase(file: UploadFile, bucket: str) -> str:
    """Upload a file to Supabase Storage and return its public URL."""
    ext = os.path.splitext(file.filename)[1].lower()
    unique_name = f"{uuid.uuid4()}{ext}"
    file_bytes = file.file.read()
    content_type = file.content_type or "application/octet-stream"
    supabase.storage.from_(bucket).upload(
        path=unique_name,
        file=file_bytes,
        file_options={"content-type": content_type, "upsert": "false"}
    )
    public_url = supabase.storage.from_(bucket).get_public_url(unique_name)
    return public_url

# Keep for backward-compatibility alias used by admin.py
def save_uploaded_file(file: UploadFile, subfolder: str) -> str:
    """Legacy alias — maps subfolder names to Supabase bucket names."""
    bucket_map = {
        "resumes": "resumes",
        "offers": "offers",
        "presentations": "presentations",
    }
    bucket = bucket_map.get(subfolder, subfolder)
    return upload_to_supabase(file, bucket)

@router.post("/apply", response_model=InternshipResponse)
async def apply_internship(
    background_tasks: BackgroundTasks,
    name: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    college: str = Form(...),
    referrer_email: str = Form(...),
    resume: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    # Check if user already exists
    existing_user = db.query(User).filter(User.email == email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email is already registered.")
        
    # Validate resume (PDF only)
    validate_file(resume, [".pdf"])
    
    # Upload resume to Supabase Storage
    resume_path = upload_to_supabase(resume, "resumes")
    
    # Check if referrer exists (Employee role)
    referrer = db.query(User).filter(User.email == referrer_email, User.role == "Employee").first()
    
    # Create User
    new_user = User(
        email=email,
        hashed_password=get_password_hash(password),
        role="Intern",
        is_active=True
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    # Create Internship application
    new_internship = Internship(
        intern_id=new_user.id,
        name=name,
        college=college,
        resume_path=resume_path,
        referrer_email=referrer_email,
        referrer_id=referrer.id if referrer else None,
        status="WAITING_EMPLOYEE"
    )
    db.add(new_internship)
    db.commit()
    db.refresh(new_internship)
    
    log_action(db, new_user.id, "APPLY", f"Intern applied. Status: WAITING_EMPLOYEE, Referrer: {referrer_email}")
    
    # Send Email to Referrer (if exists) or fallback
    email_subject = f"Action Required: Referral Request for {name}"
    email_body = f"""
    <h3>Agilisium Intern & Referral Portal (AIRP)</h3>
    <p>Hi,</p>
    <p><strong>{name}</strong> from {college} has applied for an internship and listed you as the referring employee.</p>
    <p>Please log in to the AIRP portal to review and accept/reject this referral.</p>
    <br/>
    <p>Regards,<br/>Agilisium AIRP Team</p>
    """
    send_email_background(background_tasks, db, referrer_email, email_subject, email_body)
    
    # Also notify candidate
    candidate_subject = "Internship Application Received"
    candidate_body = f"""
    <h3>Agilisium Intern & Referral Portal (AIRP)</h3>
    <p>Dear {name},</p>
    <p>Your application has been received and is waiting for employee referral approval from <strong>{referrer_email}</strong>.</p>
    <p>You can log in to your dashboard to check the status.</p>
    <br/>
    <p>Regards,<br/>Agilisium AIRP Team</p>
    """
    send_email_background(background_tasks, db, email, candidate_subject, candidate_body)
    
    return new_internship

@router.get("/details", response_model=InternshipResponse)
def get_internship_details(
    current_user: User = Depends(RoleChecker(["Intern"])),
    db: Session = Depends(get_db)
):
    internship = db.query(Internship).filter(Internship.intern_id == current_user.id).first()
    if not internship:
        raise HTTPException(status_code=404, detail="Internship profile not found")
    return internship

@router.put("/profile", response_model=InternshipResponse)
async def complete_profile(
    background_tasks: BackgroundTasks,
    name: str = Form(...),
    college: str = Form(...),
    duration_months: int = Form(...),
    tentative_start_date: str = Form(...),
    tentative_end_date: str = Form(...),
    preferred_role: str = Form(...),
    resume: Optional[UploadFile] = File(None),
    current_user: User = Depends(RoleChecker(["Intern"])),
    db: Session = Depends(get_db)
):
    internship = db.query(Internship).filter(Internship.intern_id == current_user.id).first()
    if not internship:
        raise HTTPException(status_code=404, detail="Internship profile not found")
    
    if internship.status != "REFERRAL_ACCEPTED" and internship.status != "WAITING_ADMIN":
        raise HTTPException(status_code=400, detail="Cannot edit profile in current status")
        
    internship.name = name
    internship.college = college
    internship.duration_months = duration_months
    internship.tentative_start_date = datetime.strptime(tentative_start_date, "%Y-%m-%d").date()
    internship.tentative_end_date = datetime.strptime(tentative_end_date, "%Y-%m-%d").date()
    internship.preferred_role = preferred_role
    
    if resume:
        validate_file(resume, [".pdf"])
        internship.resume_path = upload_to_supabase(resume, "resumes")
        
    internship.status = "WAITING_ADMIN"
    db.commit()
    db.refresh(internship)
    
    log_action(db, current_user.id, "COMPLETE_PROFILE", "Intern completed profile, waiting for Admin review")
    
    # Notify Admins (For now, we can notify the Super Admin or standard admin, let's find all Admins/Super Admins and email them)
    admins = db.query(User).filter(User.role.in_(["Admin", "Super Admin"])).all()
    for admin in admins:
        admin_subject = f"Pending Approval: Internship Profile for {name}"
        admin_body = f"""
        <h3>Agilisium Intern & Referral Portal (AIRP)</h3>
        <p>Dear Admin,</p>
        <p>Intern candidate <strong>{name}</strong> has completed their profile and is waiting for review.</p>
        <p>Details:</p>
        <ul>
          <li>College: {college}</li>
          <li>Role: {preferred_role}</li>
          <li>Duration: {duration_months} months</li>
        </ul>
        <p>Please log in to the portal to review and approve/reject.</p>
        <br/>
        <p>Regards,<br/>Agilisium AIRP Team</p>
        """
        send_email_background(background_tasks, db, admin.email, admin_subject, admin_body)
        
    return internship

@router.post("/offer/respond", response_model=InternshipResponse)
async def respond_to_offer(
    background_tasks: BackgroundTasks,
    response: str = Form(...),  # "ACCEPT" or "DECLINE"
    current_user: User = Depends(RoleChecker(["Intern"])),
    db: Session = Depends(get_db)
):
    internship = db.query(Internship).filter(Internship.intern_id == current_user.id).first()
    if not internship:
        raise HTTPException(status_code=404, detail="Internship profile not found")
        
    if internship.status != "OFFER_SENT":
        raise HTTPException(status_code=400, detail="No active offer to respond to")
        
    if response.upper() == "ACCEPT":
        internship.status = "ACTIVATED"
        db.commit()
        
        log_action(db, current_user.id, "OFFER_ACCEPTED", "Intern accepted the internship offer")
        
        # Onboarding Email
        onboarding_subject = "Welcome to Agilisium! Your Internship is Activated"
        onboarding_body = f"""
        <h3>Agilisium Intern & Referral Portal (AIRP)</h3>
        <p>Dear {internship.name},</p>
        <p>Congratulations! Your internship with Agilisium has been activated.</p>
        <p>Please log in to your dashboard to get started with project selection and track your attendance.</p>
        <br/>
        <p>Regards,<br/>Agilisium HR Team</p>
        """
        send_email_background(background_tasks, db, current_user.email, onboarding_subject, onboarding_body)
        
        # Notify Referrer
        if internship.referrer_email:
            referrer_subject = f"Your Referral {internship.name} has Accepted the Offer"
            referrer_body = f"""
            <h3>Agilisium Intern & Referral Portal (AIRP)</h3>
            <p>Hi,</p>
            <p>Your referral <strong>{internship.name}</strong> has accepted their internship offer and their internship is now activated.</p>
            <br/>
            <p>Regards,<br/>Agilisium AIRP Team</p>
            """
            send_email_background(background_tasks, db, internship.referrer_email, referrer_subject, referrer_body)
            
    else:
        internship.status = "OFFER_DECLINED"
        db.commit()
        
        log_action(db, current_user.id, "OFFER_DECLINED", "Intern declined the internship offer")
        
    db.refresh(internship)
    return internship

@router.post("/attendance", response_model=AttendanceResponse)
def mark_attendance(
    status: str = Form(...),  # "Present", "Absent"
    date_str: Optional[str] = Form(None),
    current_user: User = Depends(RoleChecker(["Intern"])),
    db: Session = Depends(get_db)
):
    # Check if internship is active
    internship = db.query(Internship).filter(Internship.intern_id == current_user.id).first()
    if not internship or internship.status != "ACTIVATED":
        raise HTTPException(status_code=400, detail="Internship must be ACTIVE to mark attendance")
        
    att_date = date.today()
    if date_str:
        try:
            att_date = datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid date format, use YYYY-MM-DD")
            
    # Check if already marked
    existing = db.query(Attendance).filter(
        Attendance.intern_id == current_user.id,
        Attendance.date == att_date
    ).first()
    
    if existing:
        existing.status = status
        db.commit()
        db.refresh(existing)
        log_action(db, current_user.id, "MARK_ATTENDANCE", f"Updated attendance on {att_date} to {status}")
        return existing
        
    new_attendance = Attendance(
        intern_id=current_user.id,
        date=att_date,
        status=status
    )
    db.add(new_attendance)
    db.commit()
    db.refresh(new_attendance)
    
    log_action(db, current_user.id, "MARK_ATTENDANCE", f"Marked attendance on {att_date} as {status}")
    return new_attendance

@router.get("/attendance", response_model=list[AttendanceResponse])
def get_my_attendance(
    current_user: User = Depends(RoleChecker(["Intern"])),
    db: Session = Depends(get_db)
):
    return db.query(Attendance).filter(Attendance.intern_id == current_user.id).order_by(Attendance.date.desc()).all()

@router.post("/project", response_model=ProjectResponse)
def select_project(
    project_type: str = Form(...),  # "Company" or "Own"
    company_project_id: Optional[int] = Form(None),
    own_project_title: Optional[str] = Form(None),
    own_project_description: Optional[str] = Form(None),
    current_user: User = Depends(RoleChecker(["Intern"])),
    db: Session = Depends(get_db)
):
    # Verify active internship
    internship = db.query(Internship).filter(Internship.intern_id == current_user.id).first()
    if not internship or internship.status != "ACTIVATED":
        raise HTTPException(status_code=400, detail="Internship must be ACTIVE to select project")
        
    # Check if project already exists
    existing = db.query(Project).filter(Project.intern_id == current_user.id).first()
    if existing:
        raise HTTPException(status_code=400, detail="Project already selected. Update existing project instead.")
        
    if project_type == "Company":
        if not company_project_id:
            raise HTTPException(status_code=400, detail="Company project ID is required")
        comp_proj = db.query(CompanyProject).filter(CompanyProject.id == company_project_id).first()
        if not comp_proj:
            raise HTTPException(status_code=404, detail="Company project not found")
            
        new_proj = Project(
            intern_id=current_user.id,
            project_type="Company",
            company_project_id=company_project_id,
            status="In Progress",
            progress_pct=0
        )
    else:
        if not own_project_title or not own_project_description:
            raise HTTPException(status_code=400, detail="Title and Description are required for custom project")
        new_proj = Project(
            intern_id=current_user.id,
            project_type="Own",
            own_project_title=own_project_title,
            own_project_description=own_project_description,
            status="In Progress",
            progress_pct=0
        )
        
    db.add(new_proj)
    db.commit()
    db.refresh(new_proj)
    
    log_action(db, current_user.id, "SELECT_PROJECT", f"Selected project: {project_type}")
    return new_proj

@router.get("/project", response_model=Optional[ProjectResponse])
def get_my_project(
    current_user: User = Depends(RoleChecker(["Intern"])),
    db: Session = Depends(get_db)
):
    return db.query(Project).filter(Project.intern_id == current_user.id).first()

@router.put("/project", response_model=ProjectResponse)
def update_project(
    progress_pct: int = Form(...),
    status: str = Form(...),  # "In Progress", "Completed"
    notes: Optional[str] = Form(None),
    current_user: User = Depends(RoleChecker(["Intern"])),
    db: Session = Depends(get_db)
):
    project = db.query(Project).filter(Project.intern_id == current_user.id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project selection not found")
        
    project.progress_pct = progress_pct
    project.status = status
    if notes is not None:
        project.notes = notes
        
    db.commit()
    db.refresh(project)
    
    log_action(db, current_user.id, "UPDATE_PROJECT", f"Updated project progress to {progress_pct}% status: {status}")
    return project

@router.post("/complete", response_model=InternshipResponse)
async def upload_final_presentation(
    background_tasks: BackgroundTasks,
    ppt: UploadFile = File(...),
    current_user: User = Depends(RoleChecker(["Intern"])),
    db: Session = Depends(get_db)
):
    internship = db.query(Internship).filter(Internship.intern_id == current_user.id).first()
    if not internship or internship.status != "ACTIVATED":
        raise HTTPException(status_code=400, detail="Active internship required to complete")
        
    validate_file(ppt, [".pptx", ".ppt"])
    
    # Upload final presentation to Supabase Storage
    ppt_path = upload_to_supabase(ppt, "presentations")
    
    internship.final_ppt_path = ppt_path
    # Keep status as ACTIVATED but with uploaded PPT. Admin will review and change status to COMPLETED
    db.commit()
    db.refresh(internship)
    
    log_action(db, current_user.id, "UPLOAD_FINAL_PPT", "Uploaded final presentation PPT")
    
    # Notify Admins
    admins = db.query(User).filter(User.role.in_(["Admin", "Super Admin"])).all()
    for admin in admins:
        admin_subject = f"Review Required: Final Presentation from {internship.name}"
        admin_body = f"""
        <h3>Agilisium Intern & Referral Portal (AIRP)</h3>
        <p>Dear Admin,</p>
        <p>Intern <strong>{internship.name}</strong> has uploaded their final presentation PPT.</p>
        <p>Please log in to the portal to review the presentation and mark the internship as completed.</p>
        <br/>
        <p>Regards,<br/>Agilisium AIRP Team</p>
        """
        send_email_background(background_tasks, db, admin.email, admin_subject, admin_body)
        
    return internship
