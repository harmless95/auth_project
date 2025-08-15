from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import status, HTTPException

from core.model import User
from core.schema.user import UserCreate


async def create_user(
    session: AsyncSession,
    data_user: UserCreate,
) -> User:
    stmt = select(User).where(User.email == data_user.email)
    result = await session.scalars(stmt)
    user = result.first()
    if user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Invalid there is already a user with this: {data_user.email}",
        )
    user = User(**data_user.model_dump())
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user
