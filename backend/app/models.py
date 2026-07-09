from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Date, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.core.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(String, nullable=False)  # "Super Admin", "Admin", "Employee", "Intern"
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    internship = relationship("Internship", back_populates="intern", uselist=False, foreign_keys="Internship.intern_id")
    referred_internships = relationship("Internship", back_populates="referrer", foreign_keys="Internship.referrer_id")
    attendance = relationship("Attendance", back_populates="intern")
    project = relationship("Project", back_populates="intern", uselist=False)
    audit_logs = relationship("AuditLog", back_populates="user")

class Internship(Base):
    __tablename__ = "internships"

    id = Column(Integer, primary_key=True, index=True)
    intern_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    name = Column(String, nullable=False)
    college = Column(String, nullable=False)
    duration_months = Column(Integer, nullable=True)
    tentative_start_date = Column(Date, nullable=True)
    tentative_end_date = Column(Date, nullable=True)
    preferred_role = Column(String, nullable=True)
    resume_path = Column(String, nullable=True)
    referrer_email = Column(String, nullable=False)
    referrer_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    
    # Status machine:
    # "WAITING_EMPLOYEE", "REFERRAL_REJECTED", "REFERRAL_ACCEPTED"
    # "WAITING_ADMIN", "ADMIN_REJECTED", "OFFER_SENT", "OFFER_DECLINED"
    # "ACTIVATED", "COMPLETED"
    status = Column(String, default="WAITING_EMPLOYEE", nullable=False)
    
    offer_letter_path = Column(String, nullable=True)
    final_ppt_path = Column(String, nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    intern = relationship("User", back_populates="internship", foreign_keys=[intern_id])
    referrer = relationship("User", back_populates="referred_internships", foreign_keys=[referrer_id])

class Attendance(Base):
    __tablename__ = "attendance"

    id = Column(Integer, primary_key=True, index=True)
    intern_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    date = Column(Date, nullable=False)
    status = Column(String, nullable=False)  # "Present", "Absent"
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    intern = relationship("User", back_populates="attendance")

class CompanyProject(Base):
    __tablename__ = "company_projects"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    intern_id = Column(Integer, ForeignKey("users.id"), nullable=False, unique=True)
    project_type = Column(String, nullable=False)  # "Company" or "Own"
    company_project_id = Column(Integer, ForeignKey("company_projects.id"), nullable=True)
    own_project_title = Column(String, nullable=True)
    own_project_description = Column(Text, nullable=True)
    status = Column(String, default="In Progress", nullable=False)  # "In Progress", "Completed"
    progress_pct = Column(Integer, default=0, nullable=False)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    intern = relationship("User", back_populates="project")
    company_project = relationship("CompanyProject")

class Setting(Base):
    __tablename__ = "settings"

    key = Column(String, primary_key=True, index=True)
    value = Column(String, nullable=False)

class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    action = Column(String, nullable=False)
    details = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="audit_logs")
