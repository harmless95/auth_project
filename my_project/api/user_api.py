from typing import Annotated
from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from api.dependencies.user_token import (
    auth_user,
    get_user_token,
    get_user_refresh_token,
)
from api.CRUD.crud_user import create_user
from api.dependencies.helpers import create_access_token, create_refresh_token
from core.config import setting
from core.model import db_helper
from core.schema.token import TokenBase
from core.schema.user import UserCreate, UserRead

http_bearer = HTTPBearer(auto_error=False)

router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
    dependencies=[Depends(http_bearer)],
)


@router.post(
    "/register/",
    response_model=UserRead,
    status_code=status.HTTP_201_CREATED,
)
async def register_user(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    data_user: UserCreate,
) -> UserRead:
    user = await create_user(session=session, data_user=data_user)
    return UserRead.model_validate(user)


@router.post(
    "/login/",
    response_model=TokenBase,
)
async def login(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    data_user: OAuth2PasswordRequestForm = Depends(),
):
    user = await auth_user(session=session, data_user=data_user)
    access_token = create_access_token(user=user)
    refresh_token = create_refresh_token(user=user)
    return TokenBase(
        access_token=access_token,
        refresh_token=refresh_token,
    )


@router.get("/me/")
async def user_me(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    payload: str = Depends(setting.auth_jwt.oauth2_scheme),
):
    user, payload_user = await get_user_token(session=session, token=payload)
    logged_in_at = payload_user.get("logged_in_at")
    return {
        "email": user.email,
        "name": user.name,
        "logged_in_at": logged_in_at,
    }


@router.post(
    "/refresh/",
    response_model=TokenBase,
    response_model_exclude_none=True,
)
async def refresh_jwt_token(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    data_user: str = Depends(setting.auth_jwt.oauth2_scheme),
):
    user, payload = await get_user_refresh_token(session=session, token=data_user)
    access_token = create_access_token(user=user)
    refresh_token = create_refresh_token(user=user)
    return TokenBase(
        access_token=access_token,
        refresh_token=refresh_token,
    )
