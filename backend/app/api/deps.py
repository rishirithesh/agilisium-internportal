<<<<<<< HEAD
import uuid

from fastapi import Depends, Header, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.exceptions import AuthenticationError
from app.core.permissions import Action, Role, can
from app.core.security import TokenType, decode_token
from app.models.user import User
from app.repositories.user_repository import UserRepository


async def get_current_user(
    authorization: str | None = Header(default=None), db: AsyncSession = Depends(get_db)
) -> User:
    if not authorization or not authorization.lower().startswith("bearer "):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Missing bearer token")

    token = authorization.split(" ", 1)[1]
    try:
        payload = decode_token(token)
    except ValueError as exc:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid or expired token") from exc

    if payload.get("type") != TokenType.ACCESS.value:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid token type")

    user = await UserRepository(db).get_by_id(uuid.UUID(payload["sub"]))
    if not user or not user.is_active:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "User not found or inactive")
    return user


def require_action(action: Action):
    """FastAPI dependency factory: protects a route behind a single centralized permission."""

    async def _guard(user: User = Depends(get_current_user)) -> User:
        if not can(user.role, action):
            raise HTTPException(status.HTTP_403_FORBIDDEN, f"Not permitted: {action.value}")
        return user

    return _guard


def require_role(*roles: Role):
    async def _guard(user: User = Depends(get_current_user)) -> User:
        if user.role not in roles:
            raise HTTPException(status.HTTP_403_FORBIDDEN, "Insufficient role for this resource")
        return user

    return _guard
=======
from typing import Generator, List
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import jwt

from app.core.config import settings
from app.core.database import get_db
from app.core.security import decode_access_token
from app.models import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

def get_current_user(
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    email = decode_access_token(token)
    if email is None:
        raise credentials_exception
    user = db.query(User).filter(User.email == email).first()
    if user is None:
        raise credentials_exception
    return user

def get_current_active_user(
    current_user: User = Depends(get_current_user)
) -> User:
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

class RoleChecker:
    def __init__(self, allowed_roles: List[str]):
        self.allowed_roles = allowed_roles

    def __call__(
        self,
        current_user: User = Depends(get_current_active_user)
    ) -> User:
        if current_user.role not in self.allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="The user does not have enough privileges",
            )
        return current_user
>>>>>>> master
