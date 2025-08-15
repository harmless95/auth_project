from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String

from .base import Base


class User(Base):
    email: Mapped[str] = mapped_column(
        String(length=320), unique=True, index=True, nullable=False
    )
    password_hash: Mapped[str] = mapped_column(String(1024), nullable=False)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
