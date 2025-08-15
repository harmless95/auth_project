from typing import Annotated
from datetime import datetime, timezone
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from api.crud import create_user, auth_user
from core.model import db_helper, User
from core.schema.token import TokenBase
from core.schema.user import UserCreate, UserRead, UserBase, UserLogin
from utils.validates import encode_jwt

router = APIRouter(prefix="/user", tags=["User"])


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
    token_user = encode_jwt(payload=jwt_payload)
    return TokenBase(
        access_token=token_user,
        token_type="Bearer",
    )
