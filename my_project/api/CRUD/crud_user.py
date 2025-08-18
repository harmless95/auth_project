from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from core.model import User
from core.schema.user import UserCreate
from utils.validates import hash_password


async def get_user_by_email(
    session: AsyncSession,
    email_user: str,
) -> User:
    """
    Ищем пользователя по электроной почте
    args:
        session: AsyncSession — сессия базы данных
        email_user: str - электроная почта
    return:
        user: User - Возвращаем модель User
    """
    stmt = select(User).where(User.email == email_user)
    result = await session.scalars(stmt)
    user = result.first()
    return user


async def create_user(
    session: AsyncSession,
    data_user: UserCreate,
) -> User:
    """
    Создаем user
    args:
        session: AsyncSession — сессия базы данных
        data_user: UserCreate - Данные нового пользователя
    return:
        user: User - Возвращаем модель User
    """
    # Ищем пользователя в базе данных на наличие
    user = await get_user_by_email(session=session, email_user=str(data_user.email))
    if user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Invalid there is already a user with this: {data_user.email}",
        )
    # Хэшируем пароль
    hash_bytes = hash_password(data_user.password)
    # Преобразуем пароль из байтов в строку для хранения в базе данных
    hex_hash = hash_bytes.hex()
    # Создаем пользователя
    user = User(
        email=data_user.email,
        password_hash=hex_hash,
        name=data_user.name,
    )
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user
