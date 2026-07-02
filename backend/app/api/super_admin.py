from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import get_password_hash
from app.api.deps import get_current_active_user, RoleChecker
from app.models import User, Internship, AuditLog, Setting
from app.schemas import UserResponse, UserCreate, AnalyticsResponse, SMTPConfig, AuditLogResponse
from app.services.audit_service import log_action

router = APIRouter()

@router.post("/accounts", response_model=UserResponse)
def create_account(
    user_in: UserCreate,
    current_user: User = Depends(RoleChecker(["Super Admin"])),
    db: Session = Depends(get_db)
):
    if user_in.role not in ["Admin", "Employee"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Super Admin can only create Admin and Employee accounts"
        )
        
    existing_user = db.query(User).filter(User.email == user_in.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="An account with this email already exists"
        )
        
    new_user = User(
        email=user_in.email,
        hashed_password=get_password_hash(user_in.password),
        role=user_in.role,
        is_active=user_in.is_active
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    log_action(db, current_user.id, "CREATE_ACCOUNT", f"Created {user_in.role} account: {user_in.email}")
    return new_user

@router.get("/accounts", response_model=list[UserResponse])
def get_accounts(
    current_user: User = Depends(RoleChecker(["Super Admin"])),
    db: Session = Depends(get_db)
):
    return db.query(User).filter(User.role.in_(["Admin", "Employee"])).all()

@router.get("/analytics", response_model=AnalyticsResponse)
def get_analytics(
    current_user: User = Depends(RoleChecker(["Super Admin"])),
    db: Session = Depends(get_db)
):
    total_apps = db.query(Internship).count()
    pending_ref = db.query(Internship).filter(Internship.status == "WAITING_EMPLOYEE").count()
    active_int = db.query(Internship).filter(Internship.status == "ACTIVATED").count()
    completed_int = db.query(Internship).filter(Internship.status == "COMPLETED").count()
    
    # Status breakdown
    all_internships = db.query(Internship.status).all()
    by_status = {}
    for (status_val,) in all_internships:
        by_status[status_val] = by_status.get(status_val, 0) + 1
        
    return {
        "total_applications": total_apps,
        "pending_referrals": pending_ref,
        "active_interns": active_int,
        "completed_internships": completed_int,
        "by_status": by_status
    }

@router.get("/audit-logs", response_model=list[AuditLogResponse])
def get_audit_logs(
    current_user: User = Depends(RoleChecker(["Super Admin"])),
    db: Session = Depends(get_db)
):
    logs = db.query(AuditLog).order_by(AuditLog.created_at.desc()).all()
    
    response_logs = []
    for log in logs:
        user_email = None
        if log.user_id:
            usr = db.query(User).filter(User.id == log.user_id).first()
            if usr:
                user_email = usr.email
        response_logs.append({
            "id": log.id,
            "user_id": log.user_id,
            "action": log.action,
            "details": log.details,
            "created_at": log.created_at,
            "user_email": user_email
        })
        
    return response_logs

@router.get("/smtp", response_model=SMTPConfig)
def get_smtp_config(
    current_user: User = Depends(RoleChecker(["Super Admin"])),
    db: Session = Depends(get_db)
):
    # Retrieve SMTP settings
    from app.core.config import settings
    
    host = db.query(Setting).filter(Setting.key == "smtp_host").first()
    port = db.query(Setting).filter(Setting.key == "smtp_port").first()
    user = db.query(Setting).filter(Setting.key == "smtp_user").first()
    password = db.query(Setting).filter(Setting.key == "smtp_pass").first()
    from_email = db.query(Setting).filter(Setting.key == "smtp_from").first()
    
    return {
        "host": host.value if host else settings.SMTP_HOST,
        "port": int(port.value) if port else settings.SMTP_PORT,
        "user": user.value if user else settings.SMTP_USER,
        "password": password.value if password else settings.SMTP_PASS,
        "from_email": from_email.value if from_email else settings.SMTP_FROM,
    }

@router.post("/smtp", status_code=204)
def update_smtp_config(
    smtp_in: SMTPConfig,
    current_user: User = Depends(RoleChecker(["Super Admin"])),
    db: Session = Depends(get_db)
):
    def set_config(key: str, val: str):
        db_setting = db.query(Setting).filter(Setting.key == key).first()
        if db_setting:
            db_setting.value = val
        else:
            db_setting = Setting(key=key, value=val)
            db.add(db_setting)
            
    set_config("smtp_host", smtp_in.host)
    set_config("smtp_port", str(smtp_in.port))
    set_config("smtp_user", smtp_in.user)
    set_config("smtp_pass", smtp_in.password)
    set_config("smtp_from", smtp_in.from_email)
    
    db.commit()
    log_action(db, current_user.id, "UPDATE_SMTP_CONFIG", "Updated system SMTP configuration settings")
    return
