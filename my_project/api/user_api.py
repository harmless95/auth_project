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
    now = datetime.now(timezone.utc)
    jwt_payload = {
        "sub": user.email,
        "email": user.email,
        "name": user.name,
        "logged_in_at": now.isoformat(),
    }
    token_user = encode_jwt(
        payload=jwt_payload,
        private_key=setting.auth_jwt.private_key_path.read_text(),
        algorithm=setting.auth_jwt.algorithm,
        expire_minutes=setting.auth_jwt.access_token_expire_minutes,
    )
    return TokenBase(
        access_token=token_user,
        token_type="Bearer",
    )


@router.get("/me/")
async def user_me(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    payload: str = Depends(setting.auth_jwt.oauth2_scheme),
):
    user = await get_user_token(session=session, token=payload)
    return user
