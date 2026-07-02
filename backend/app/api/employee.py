from fastapi import APIRouter, Depends, HTTPException, Form, BackgroundTasks
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.api.deps import get_current_active_user, RoleChecker
from app.models import User, Internship
from app.schemas import InternshipResponse
from app.services.email_service import send_email_background
from app.services.audit_service import log_action

router = APIRouter()

@router.get("/referrals", response_model=list[InternshipResponse])
def get_my_referrals(
    current_user: User = Depends(RoleChecker(["Employee"])),
    db: Session = Depends(get_db)
):
    # Match by referrer_email or referrer_id
    referrals = db.query(Internship).filter(
        (Internship.referrer_email == current_user.email) | (Internship.referrer_id == current_user.id)
    ).order_by(Internship.created_at.desc()).all()
    return referrals

@router.post("/referrals/{internship_id}/respond", response_model=InternshipResponse)
async def respond_referral(
    internship_id: int,
    background_tasks: BackgroundTasks,
    response: str = Form(...),  # "ACCEPT" or "REJECT"
    current_user: User = Depends(RoleChecker(["Employee"])),
    db: Session = Depends(get_db)
):
    internship = db.query(Internship).filter(
        Internship.id == internship_id,
        (Internship.referrer_email == current_user.email) | (Internship.referrer_id == current_user.id)
    ).first()
    
    if not internship:
        raise HTTPException(status_code=404, detail="Referral request not found")
        
    if internship.status != "WAITING_EMPLOYEE":
        raise HTTPException(status_code=400, detail="Referral is already processed")
        
    # Associate referrer_id if not done yet
    if not internship.referrer_id:
        internship.referrer_id = current_user.id
        
    # Find intern email
    intern_user = db.query(User).filter(User.id == internship.intern_id).first()
    
    if response.upper() == "ACCEPT":
        internship.status = "REFERRAL_ACCEPTED"
        db.commit()
        
        log_action(db, current_user.id, "REFERRAL_ACCEPTED", f"Accepted referral for {internship.name}")
        
        # Email to intern
        subject = "Your Employee Referral has been Approved!"
        body = f"""
        <h3>Agilisium Intern & Referral Portal (AIRP)</h3>
        <p>Dear {internship.name},</p>
        <p>Good news! Your referral from <strong>{current_user.email}</strong> has been approved.</p>
        <p>Please log in to your dashboard to complete your internship profile and submit it for admin review.</p>
        <br/>
        <p>Regards,<br/>Agilisium AIRP Team</p>
        """
        send_email_background(background_tasks, db, intern_user.email, subject, body)
    else:
        internship.status = "REFERRAL_REJECTED"
        db.commit()
        
        log_action(db, current_user.id, "REFERRAL_REJECTED", f"Rejected referral for {internship.name}")
        
        # Email to intern
        subject = "Referral Update: Application Status"
        body = f"""
        <h3>Agilisium Intern & Referral Portal (AIRP)</h3>
        <p>Dear {internship.name},</p>
        <p>Thank you for your interest in Agilisium.</p>
        <p>Unfortunately, your referral request was not approved by the employee. Your application cannot proceed further at this time.</p>
        <br/>
        <p>Regards,<br/>Agilisium AIRP Team</p>
        """
        send_email_background(background_tasks, db, intern_user.email, subject, body)
        
    db.refresh(internship)
    return internship
