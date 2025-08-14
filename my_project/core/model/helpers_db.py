from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    AsyncSession,
)

from core.config import setting


class DatabaseHelper:
    def __init__(
        self,
        url: str,
        echo: bool,
    ):
        self.create_engine = create_async_engine(
            url=url,
            echo=echo,
        )
        self.fabric_session = async_sessionmaker(
            bind=self.create_engine,
            autoflush=False,
            expire_on_commit=False,
        )

    async def dispose(self) -> None:
        await self.create_engine.dispose()

    async def session_getter(self) -> AsyncGenerator[AsyncSession | None]:
        async with self.fabric_session() as session:
            yield session
            await session.close()


db_helper = DatabaseHelper(
    url=str(setting.db.url),
    echo=setting.db.echo,
)
