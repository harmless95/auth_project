from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import status, HTTPException, Depends

from core.model import User, db_helper
from core.schema.user import UserCreate, UserBase
from utils.validates import hash_password, validates_password


async def get_user_by_email(
    session: AsyncSession,
    email_user: str,
) -> User:
    stmt = select(User).where(User.email == email_user)
    result = await session.scalars(stmt)
    user = result.first()
    return user


async def create_user(
    session: AsyncSession,
    data_user: UserCreate,
) -> User:
    user = await get_user_by_email(session=session, email_user=str(data_user.email))
    if user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Invalid there is already a user with this: {data_user.email}",
        )
    hash_bytes = hash_password(data_user.password)
    hex_hash = hash_bytes.hex()
    user = User(
        email=data_user.email,
        password_hash=hex_hash,
        name=data_user.name,
    )
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user


async def auth_user(
    data_user: UserBase,
    session: AsyncSession = Depends(db_helper.session_getter),
) -> User:
    error_ex = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="User not found or invalid credentials",
    )
    user = await get_user_by_email(session=session, email_user=str(data_user.email))
    if not user:
        raise error_ex

    user_password = validates_password(
        password=data_user.password,
        password_hash=user.password_hash,
    )
    if not user_password:
        raise error_ex
    return user
