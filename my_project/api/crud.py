from sqlalchemy.ext.asyncio import AsyncSession

from core.model import User
from core.schema.user import UserCreate


async def create_user(
    session: AsyncSession,
    data_user: UserCreate,
) -> User:
    user = User(**data_user.model_dump())
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user
