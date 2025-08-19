from typing import AsyncGenerator

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.application.services.task_service import TaskService
from src.domain.repositories.tasks import ITaskRepository
from src.infrastructure.database.connection import async_session
from src.infrastructure.persistence.sqlalchemy.task_repository import SQLAlchemyTaskRepository


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        try:
            yield session
        finally:
            await session.close()


def get_task_repository_impl(db_session: AsyncSession = Depends(get_db_session)) -> ITaskRepository:
    return SQLAlchemyTaskRepository(db_session=db_session)


def get_task_service_impl(task_repo: ITaskRepository = Depends(get_task_repository_impl)) -> TaskService:
    return TaskService(task_repo=task_repo)
