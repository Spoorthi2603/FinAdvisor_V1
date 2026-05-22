import secrets
import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.models.user import User
from app.schemas.auth import AuthLogin, AuthRegister, AuthResponse
from app.utils.security import hash_password, verify_password

router = APIRouter(prefix="/api/v1/auth", tags=["auth"])


def _generate_customer_id() -> str:
    return f"CUST{uuid.uuid4().int % 10**8:08d}"


def _generate_sms_key() -> str:
    return secrets.token_urlsafe(32)


@router.post("/register", response_model=AuthResponse)
async def register(payload: AuthRegister, db: AsyncSession = Depends(get_db)) -> AuthResponse:
    if payload.password != payload.confirm_password:
        raise HTTPException(status_code=400, detail="Passwords do not match")

    existing = await db.execute(select(User).where(User.email == payload.email))
    if existing.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Email already registered")

    customer_id = _generate_customer_id()
    user = User(
        customer_id=customer_id,
        full_name=payload.full_name,
        email=payload.email,
        phone_number=payload.phone_number,
        password_hash=hash_password(payload.password),
        sms_webhook_key=_generate_sms_key(),
        registration_step=2,
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return AuthResponse(
        user_id=user.id,
        customer_id=user.customer_id,
        full_name=user.full_name,
        email=user.email,
    )


@router.post("/login", response_model=AuthResponse)
async def login(payload: AuthLogin, db: AsyncSession = Depends(get_db)) -> AuthResponse:
    result = await db.execute(select(User).where(User.email == payload.email))
    user = result.scalar_one_or_none()
    if not user or not user.password_hash:
        raise HTTPException(status_code=401, detail="Invalid email or password")

    password_verified, replacement_hash = verify_password(payload.password, user.password_hash)
    if not password_verified:
        raise HTTPException(status_code=401, detail="Invalid email or password")

    if replacement_hash:
        user.password_hash = replacement_hash
        await db.commit()

    return AuthResponse(
        user_id=user.id,
        customer_id=user.customer_id,
        full_name=user.full_name,
        email=user.email,
    )
