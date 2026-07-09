from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime, date

# --- Token Schemas ---
class Token(BaseModel):
    access_token: str
    token_type: str
    role: str
    email: str

class TokenData(BaseModel):
    email: Optional[str] = None

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

# --- User Schemas ---
class UserBase(BaseModel):
    email: EmailStr
    role: str
    is_active: Optional[bool] = True

class UserCreate(UserBase):
    password: str

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    role: str
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True

# --- Internship Schemas ---
class InternshipBase(BaseModel):
    name: str
    college: str
    referrer_email: EmailStr

class InternshipCreate(InternshipBase):
    password: str  # For temporary account creation

class InternshipProfileUpdate(BaseModel):
    name: str
    college: str
    duration_months: int
    tentative_start_date: date
    tentative_end_date: date
    preferred_role: str

class InternshipResponse(BaseModel):
    id: int
    intern_id: int
    name: str
    college: str
    duration_months: Optional[int] = None
    tentative_start_date: Optional[date] = None
    tentative_end_date: Optional[date] = None
    preferred_role: Optional[str] = None
    resume_path: Optional[str] = None
    referrer_email: str
    referrer_id: Optional[int] = None
    status: str
    offer_letter_path: Optional[str] = None
    final_ppt_path: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# --- Attendance Schemas ---
class AttendanceCreate(BaseModel):
    date: date
    status: str  # "Present", "Absent"

class AttendanceResponse(BaseModel):
    id: int
    intern_id: int
    date: date
    status: str
    created_at: datetime

    class Config:
        from_attributes = True

# --- Company Project Schemas ---
class CompanyProjectCreate(BaseModel):
    title: str
    description: str

class CompanyProjectResponse(BaseModel):
    id: int
    title: str
    description: str
    created_at: datetime

    class Config:
        from_attributes = True

# --- Project Selection & Tracking Schemas ---
class ProjectCreate(BaseModel):
    project_type: str  # "Company" or "Own"
    company_project_id: Optional[int] = None
    own_project_title: Optional[str] = None
    own_project_description: Optional[str] = None

class ProjectUpdate(BaseModel):
    progress_pct: int
    status: str  # "In Progress", "Completed"
    notes: Optional[str] = None

class ProjectResponse(BaseModel):
    id: int
    intern_id: int
    project_type: str
    company_project_id: Optional[int] = None
    own_project_title: Optional[str] = None
    own_project_description: Optional[str] = None
    status: str
    progress_pct: int
    notes: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    company_project: Optional[CompanyProjectResponse] = None

    class Config:
        from_attributes = True

# --- Setting & SMTP Configuration ---
class SMTPConfig(BaseModel):
    host: str
    port: int
    user: str
    password: str
    from_email: str

class SettingResponse(BaseModel):
    key: str
    value: str

    class Config:
        from_attributes = True

# --- Audit Log Schemas ---
class AuditLogResponse(BaseModel):
    id: int
    user_id: Optional[int] = None
    action: str
    details: Optional[str] = None
    created_at: datetime
    user_email: Optional[str] = None

    class Config:
        from_attributes = True

# --- Analytics Response ---
class AnalyticsResponse(BaseModel):
    total_applications: int
    pending_referrals: int
    active_interns: int
    completed_internships: int
    by_status: dict
