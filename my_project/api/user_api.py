from typing import Annotated
from datetime import datetime, timezone
from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from api.crud import create_user, auth_user, get_current_token_payload
from core.config import setting
from core.model import db_helper, User
from core.schema.token import TokenBase
from core.schema.user import UserCreate, UserRead, UserBase, UserLogin
from utils.validates import encode_jwt

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post(
    "/register",
    response_model=UserRead,
    status_code=status.HTTP_201_CREATED,
)
async def register_user(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    data_user: UserCreate,
) -> UserRead:
    user = await create_user(session=session, data_user=data_user)
    return UserRead.model_validate(user)


@router.post("/login", response_model=TokenBase)
async def login(user: UserLogin = Depends(auth_user)):
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


@router.get("/me")
async def user_me(
    payload: str = Depends(get_current_token_payload),
):
    # return {
    #     "email": payload.get("email"),
    #     "name": payload.get("name"),
    #     "logged_in_at": payload.get("logged_in_at"),
    # }
    return {"token": payload}
