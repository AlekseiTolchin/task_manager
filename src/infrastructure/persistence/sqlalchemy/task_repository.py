from typing import List, Optional
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src.domain.models.tasks import Task
from src.domain.enums.task_status import TaskStatus
from src.domain.repositories.tasks import ITaskRepository, TaskCreateData, TaskUpdateData
from src.infrastructure.persistence.sqlalchemy.models import TaskORM


class SQLAlchemyTaskRepository(ITaskRepository):
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    def _to_domain_model(self, orm_model: TaskORM) -> Optional[Task]:
        if not orm_model:
            return None
        return Task(
            id=orm_model.id,
            title=orm_model.title,
            description=orm_model.description,
            status=TaskStatus(orm_model.status),
            created_at=orm_model.created_at,
            updated_at=orm_model.updated_at,
        )

    def _to_orm_model(self, data: TaskCreateData) -> TaskORM:
        return TaskORM(
            title=data.title,
            description=data.description,
            status=TaskStatus.CREATED.value,
        )

    async def create(self, task: TaskCreateData) -> Task:
        task_orm = self._to_orm_model(task)
        self.db_session.add(task_orm)
        await self.db_session.commit()
        await self.db_session.refresh(task_orm)
        return self._to_domain_model(task_orm)

    async def get_by_id(self, task_id: UUID) -> Optional[Task]:
        orm_task = await self.db_session.scalar(select(TaskORM).where(TaskORM.id == task_id))
        return self._to_domain_model(orm_task)

    async def get_all(self) -> List[Task]:
        res = await self.db_session.scalars(select(TaskORM))
        orm_tasks = list(res.all())
        return [self._to_domain_model(post) for post in orm_tasks]

    async def update(self, task_id: UUID, task: TaskUpdateData) -> Optional[Task]:
        orm_task = await self.db_session.scalar(select(TaskORM).where(TaskORM.id == task_id))
        if not orm_task:
            return None
        orm_task.title = task.title
        orm_task.description = task.description
        orm_task.status = task.status
        await self.db_session.commit()
        await self.db_session.refresh(orm_task)
        return self._to_domain_model(orm_task)

    async def delete(self, task_id: UUID) -> bool:
        orm_task = await self.db_session.scalar(select(TaskORM).where(TaskORM.id == task_id))
        if not orm_task:
            return False
        await self.db_session.delete(orm_task)
        await self.db_session.commit()

        return True
