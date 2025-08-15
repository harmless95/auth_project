from typing import Annotated
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from api.crud import create_user
from core.model import db_helper, User
from core.schema.user import UserCreate, UserRead

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
    return user
