from typing import Annotated
from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from api.crud import create_user, auth_user, get_current_token_payload, get_user_token
from core.config import setting
from core.model import db_helper, User
from core.schema.token import TokenBase
from core.schema.user import UserCreate, UserRead, UserBase, UserLogin
from utils.validates import encode_jwt

router = APIRouter(prefix="/auth", tags=["Auth"])


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
    user = await get_user_token(session=session, token=payload)
    return user
