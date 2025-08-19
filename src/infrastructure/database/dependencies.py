from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession

from src.infrastructure.database.connection import async_session


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        try:
            yield session
        finally:
            await session.close()
