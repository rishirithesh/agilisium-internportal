import os
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, BackgroundTasks, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.api.deps import get_current_active_user, RoleChecker
from app.models import User, Internship, Attendance, Project, CompanyProject
from app.schemas import InternshipResponse, CompanyProjectResponse, CompanyProjectCreate, ProjectResponse, AttendanceResponse
from app.services.email_service import send_email_background
from app.services.audit_service import log_action
from app.api.intern import validate_file, save_uploaded_file

router = APIRouter()

@router.get("/applications", response_model=list[InternshipResponse])
def list_applications(
    current_user: User = Depends(RoleChecker(["Admin", "Super Admin"])),
    db: Session = Depends(get_db)
):
    return db.query(Internship).order_by(Internship.created_at.desc()).all()

@router.post("/applications/{id}/approve", response_model=InternshipResponse)
async def approve_application(
    id: int,
    background_tasks: BackgroundTasks,
    offer_letter: UploadFile = File(...),
    current_user: User = Depends(RoleChecker(["Admin", "Super Admin"])),
    db: Session = Depends(get_db)
):
    internship = db.query(Internship).filter(Internship.id == id).first()
    if not internship:
        raise HTTPException(status_code=404, detail="Application not found")
        
    if internship.status != "WAITING_ADMIN":
        raise HTTPException(status_code=400, detail="Application is not waiting for admin review")
        
    validate_file(offer_letter, [".pdf"])
    offer_path = save_uploaded_file(offer_letter, "offers")
    
    internship.offer_letter_path = offer_path
    internship.status = "OFFER_SENT"
    db.commit()
    db.refresh(internship)
    
    log_action(db, current_user.id, "APPROVE_APPLICATION", f"Approved intern application {id} and sent offer letter")
    
    # Notify Intern
    intern_user = db.query(User).filter(User.id == internship.intern_id).first()
    email_subject = "Congratulations! Internship Offer from Agilisium"
    email_body = f"""
    <h3>Agilisium Intern & Referral Portal (AIRP)</h3>
    <p>Dear {internship.name},</p>
    <p>We are pleased to offer you an internship at Agilisium! Your profile has been approved.</p>
    <p>Please log in to your dashboard to view the offer letter and respond to the offer.</p>
    <br/>
    <p>Regards,<br/>Agilisium HR Team</p>
    """
    send_email_background(background_tasks, db, intern_user.email, email_subject, email_body)
    
    return internship

@router.post("/applications/{id}/reject", response_model=InternshipResponse)
async def reject_application(
    id: int,
    background_tasks: BackgroundTasks,
    reason: str = Form(...),
    current_user: User = Depends(RoleChecker(["Admin", "Super Admin"])),
    db: Session = Depends(get_db)
):
    internship = db.query(Internship).filter(Internship.id == id).first()
    if not internship:
        raise HTTPException(status_code=404, detail="Application not found")
        
    if internship.status != "WAITING_ADMIN":
        raise HTTPException(status_code=400, detail="Application is not waiting for admin review")
        
    internship.status = "ADMIN_REJECTED"
    db.commit()
    db.refresh(internship)
    
    log_action(db, current_user.id, "REJECT_APPLICATION", f"Rejected intern application {id}. Reason: {reason}")
    
    # Notify Intern
    intern_user = db.query(User).filter(User.id == internship.intern_id).first()
    email_subject = "Update on your Internship Application"
    email_body = f"""
    <h3>Agilisium Intern & Referral Portal (AIRP)</h3>
    <p>Dear {internship.name},</p>
    <p>Thank you for taking the time to complete your internship profile.</p>
    <p>Unfortunately, your profile did not meet our criteria for the role at this time, and we cannot move forward with your application.</p>
    <p><strong>Feedback:</strong> {reason}</p>
    <br/>
    <p>Regards,<br/>Agilisium HR Team</p>
    """
    send_email_background(background_tasks, db, intern_user.email, email_subject, email_body)
    
    return internship

# --- Company Projects Management ---
@router.post("/company-projects", response_model=CompanyProjectResponse)
def create_company_project(
    project_in: CompanyProjectCreate,
    current_user: User = Depends(RoleChecker(["Admin", "Super Admin"])),
    db: Session = Depends(get_db)
):
    new_proj = CompanyProject(
        title=project_in.title,
        description=project_in.description
    )
    db.add(new_proj)
    db.commit()
    db.refresh(new_proj)
    log_action(db, current_user.id, "CREATE_COMPANY_PROJECT", f"Created company project: {project_in.title}")
    return new_proj

@router.get("/company-projects", response_model=list[CompanyProjectResponse])
def get_company_projects(
    current_user: User = Depends(RoleChecker(["Admin", "Super Admin", "Intern"])),
    db: Session = Depends(get_db)
):
    return db.query(CompanyProject).all()

@router.delete("/company-projects/{id}", status_code=204)
def delete_company_project(
    id: int,
    current_user: User = Depends(RoleChecker(["Admin", "Super Admin"])),
    db: Session = Depends(get_db)
):
    comp_proj = db.query(CompanyProject).filter(CompanyProject.id == id).first()
    if not comp_proj:
        raise HTTPException(status_code=404, detail="Company project not found")
        
    db.delete(comp_proj)
    db.commit()
    log_action(db, current_user.id, "DELETE_COMPANY_PROJECT", f"Deleted project ID {id}")
    return

# --- Intern Tracking ---
@router.get("/intern-projects", response_model=list[ProjectResponse])
def get_intern_projects(
    current_user: User = Depends(RoleChecker(["Admin", "Super Admin"])),
    db: Session = Depends(get_db)
):
    return db.query(Project).all()

@router.get("/attendance", response_model=list[AttendanceResponse])
def get_all_attendance(
    current_user: User = Depends(RoleChecker(["Admin", "Super Admin"])),
    db: Session = Depends(get_db)
):
    return db.query(Attendance).order_by(Attendance.date.desc()).all()

@router.post("/internships/{id}/complete", response_model=InternshipResponse)
async def complete_internship(
    id: int,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(RoleChecker(["Admin", "Super Admin"])),
    db: Session = Depends(get_db)
):
    internship = db.query(Internship).filter(Internship.id == id).first()
    if not internship:
        raise HTTPException(status_code=404, detail="Internship not found")
        
    if internship.status != "ACTIVATED":
        raise HTTPException(status_code=400, detail="Only activated internships can be completed")
        
    if not internship.final_ppt_path:
        raise HTTPException(status_code=400, detail="Cannot complete internship without a uploaded final presentation")
        
    internship.status = "COMPLETED"
    db.commit()
    db.refresh(internship)
    
    log_action(db, current_user.id, "COMPLETE_INTERNSHIP", f"Marked internship {id} as completed")
    
    # Notify Intern
    intern_user = db.query(User).filter(User.id == internship.intern_id).first()
    email_subject = "Congratulations on Completing your Internship at Agilisium!"
    email_body = f"""
    <h3>Agilisium Intern & Referral Portal (AIRP)</h3>
    <p>Dear {internship.name},</p>
    <p>Congratulations! Your internship project has been reviewed, and your internship has been marked as <strong>completed</strong>.</p>
    <p>Thank you for your hard work and contribution to Agilisium. We wish you all the best in your future endeavors!</p>
    <br/>
    <p>Regards,<br/>Agilisium HR Team</p>
    """
    send_email_background(background_tasks, db, intern_user.email, email_subject, email_body)
    
    return internship
