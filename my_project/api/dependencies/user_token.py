from typing import Optional, Tuple

from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import status, HTTPException
from fastapi.security import (
    OAuth2PasswordBearer,
    HTTPBearer,
    OAuth2PasswordRequestForm,
)
from jwt.exceptions import InvalidTokenError

from api.CRUD.crud_user import get_user_by_email
from core.config import setting
from core.model import User
from utils.validates import validates_password, decode_jwt

conn = HTTPBearer()
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/login/",
)


async def auth_user(
    data_user: OAuth2PasswordRequestForm,
    session: AsyncSession,
) -> User:
    """
    Проверяем user
    args:
        data_user: OAuth2PasswordRequestForm - Получаем user из формы
        session: AsyncSession — сессия базы данных
    return:
        user: User - Возвращаем модель User
    """
    error_ex = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="User not found or invalid credentials",
    )
    # Ищем пользователя в базе данных
    user = await get_user_by_email(session=session, email_user=str(data_user.username))
    if not user:
        raise error_ex
    # Сравниваем пароль
    user_password = validates_password(
        password=data_user.password,
        password_hash=user.password_hash,
    )
    if not user_password:
        raise error_ex
    return user


def validate_type_token(
    token_type: str,
    payload: dict,
) -> bool:
    """
    Проверяем тип токена
    args:
        token_type: str - Тип(type) токена
        payload: dict - Словарь из расшифрованого токена
    return:
        bool — True, если тип токена валиден, иначе выбрасывает HTTPException
    """
    payload_type = payload.get(setting.auth_jwt.type_payload)
    if payload_type == token_type:
        return True

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=f"Invalid token type {payload_type!r} expected {token_type!r}",
    )


async def validate_payload(
    token: str,
) -> dict:
    """
    Деккодируем токен
    args:
        token: str - Токен
    return:
        payload: dict - Словарь расшифрованого токена
    """
    # Исключение в случае ошибки
    error_ex = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid token",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        # Расшифровываем токен
        payload = decode_jwt(
            token=token,
            public_key=setting.auth_jwt.public_key_path.read_text(),
            algorithm=setting.auth_jwt.algorithm,
        )
        user_email = payload.get("sub")
        # Проверяем на наличие поля
        if not user_email:
            raise error_ex
    except InvalidTokenError:
        raise error_ex
    return payload


async def get_user_payload_syb(
    session: AsyncSession,
    token: str,
    token_type: str,
) -> Optional[Tuple[User, dict]]:
    """
    Получение access токена
    args:
        session: AsyncSession — сессия базы данных
        token: str — токен для проверки
        token_type: str - Тип(type) токена
    return:
        user_result, payload: Optional[Tuple[User, dict]] - Получаем пользователя и словарь расшифрованого токена
    """
    # Проверяем токен расшифровав
    payload = await validate_payload(token=token)
    user_email = payload.get("sub")
    # Проверяем на валидность типа токена
    validate_type_token(token_type=token_type, payload=payload)
    # Ищем пользователя в базе данных
    user_result = await get_user_by_email(session=session, email_user=user_email)
    if not user_result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Invalid {user_email} not found",
        )
    return user_result, payload


async def get_user_token(
    session: AsyncSession,
    token: str,
) -> Optional[Tuple[User, dict]]:
    """
    Получение access токена
    args:
        session: AsyncSession — сессия базы данных
        token: str — токен для проверки
    return:
        user_result, payload: user_result, payload: Optional[Tuple[User, dict]] - Получаем пользователя и словарь расшифрованого токена
    """
    access_type = setting.auth_jwt.type_access
    return await get_user_payload_syb(
        session=session,
        token=token,
        token_type=access_type,
    )


async def get_user_refresh_token(
    session: AsyncSession,
    token: str,
) -> Optional[Tuple[User, dict]]:
    """
    Получение refresh токена
    args:
        session: AsyncSession — сессия базы данных
        token: str — токен для проверки
    return:
        user_result, payload: Optional[Tuple[User, dict]] - Получаем пользователя и словарь расшифрованого токена
    """
    refresh_type = setting.auth_jwt.type_refresh
    return await get_user_payload_syb(
        session=session, token=token, token_type=refresh_type
    )
