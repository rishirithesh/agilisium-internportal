<<<<<<< HEAD
"""
Run with: python -m app.scripts.seed
Creates one demo user per role so the workflow slice can be exercised end-to-end.
"""
import asyncio

from app.core.database import AsyncSessionLocal
from app.core.permissions import Role
from app.core.security import hash_password
from app.models.user import User
from app.repositories.user_repository import UserRepository

DEMO_PASSWORD = "ChangeMe123!"

DEMO_USERS = [
    ("employee@airp.local", "Emma Employee", Role.EMPLOYEE),
    ("intern@airp.local", "Ian Intern", Role.INTERN),
    ("admin@airp.local", "Ava Admin", Role.ADMIN),
    ("mainadmin@airp.local", "Max MainAdmin", Role.MAIN_ADMIN),
]


async def seed() -> None:
    async with AsyncSessionLocal() as db:
        repo = UserRepository(db)
        for email, full_name, role in DEMO_USERS:
            existing = await repo.get_by_email(email)
            if existing:
                print(f"skip (exists): {email}")
                continue
            user = User(
                email=email,
                full_name=full_name,
                hashed_password=hash_password(DEMO_PASSWORD),
                role=role,
                is_active=True,
                is_email_verified=True,
            )
            await repo.create(user)
            print(f"created: {email} / {DEMO_PASSWORD} ({role})")
        await db.commit()


if __name__ == "__main__":
    asyncio.run(seed())
=======
import sys
import os

# Add parent directory to sys.path so we can import app
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from sqlalchemy.orm import Session
from app.core.database import SessionLocal, Base, engine
from app.core.security import get_password_hash
from app.models import User, CompanyProject, Setting

def seed_db():
    print("Dropping existing tables if any...")
    Base.metadata.drop_all(bind=engine)
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully.")

    db = SessionLocal()
    try:
        # 1. Create Super Admin
        super_admin_email = "admin@agilisium.com"
        admin_user = db.query(User).filter(User.email == super_admin_email).first()
        if not admin_user:
            admin_user = User(
                email=super_admin_email,
                hashed_password=get_password_hash("Admin@123"),
                role="Super Admin",
                is_active=True
            )
            db.add(admin_user)
            print(f"Super Admin account created: {super_admin_email} (Password: Admin@123)")
        else:
            print("Super Admin account already exists.")

        # 2. Create Sample Employees
        employees = [
            ("emp1@agilisium.com", "Employee@123"),
            ("emp2@agilisium.com", "Employee@123"),
            ("emp3@agilisium.com", "Employee@123")
        ]
        for email, pwd in employees:
            emp = db.query(User).filter(User.email == email).first()
            if not emp:
                emp = User(
                    email=email,
                    hashed_password=get_password_hash(pwd),
                    role="Employee",
                    is_active=True
                )
                db.add(emp)
                print(f"Employee account created: {email} (Password: {pwd})")
            else:
                print(f"Employee account already exists: {email}")

        # 3. Create Sample Admins
        admins = [
            ("hr_admin@agilisium.com", "Admin@123")
        ]
        for email, pwd in admins:
            adm = db.query(User).filter(User.role == "Admin", User.email == email).first()
            if not adm:
                adm = User(
                    email=email,
                    hashed_password=get_password_hash(pwd),
                    role="Admin",
                    is_active=True
                )
                db.add(adm)
                print(f"Admin account created: {email} (Password: {pwd})")
            else:
                print(f"Admin account already exists: {email}")

        # 4. Create Sample Company Projects
        projects = [
            ("AI-driven Talent Analytics Platform", "Build a dashboard using Python and NLP to analyze applicant resumes, score their fit against job descriptions, and predict candidate success rates using machine learning models."),
            ("Enterprise Cloud Migration Dashboard", "Develop a real-time monitor interface for tracking multi-cloud migration progress, including cost savings analysis, resource utilization, and automated compliance checking."),
            ("Next-gen Employee Learning Management System (LMS)", "Create a responsive React portal for employees to complete certification courses, take quizzes, view leaderboard statistics, and request physical training assets.")
        ]
        for title, desc in projects:
            proj = db.query(CompanyProject).filter(CompanyProject.title == title).first()
            if not proj:
                proj = CompanyProject(title=title, description=desc)
                db.add(proj)
                print(f"Company project created: {title}")
            else:
                print(f"Company project already exists: {title}")

        db.commit()
        print("Database seeding completed successfully.")
    except Exception as e:
        db.rollback()
        print(f"Seeding failed: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    seed_db()
>>>>>>> master
