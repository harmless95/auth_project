from typing import Annotated
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.crud import create_user
from core.model import db_helper
from core.schema.user import UserCreate, UserRead

router = APIRouter(prefix="/user", tags=["User"])


@router.post("/")
async def register_user(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    data_user: UserCreate,
) -> UserRead:
    return await create_user(session=session, data_user=data_user)
