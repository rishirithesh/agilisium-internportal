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
