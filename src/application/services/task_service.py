from typing import List, Optional
from uuid import UUID

from src.domain.models.tasks import Task
from src.domain.repositories.tasks import ITaskRepository, TaskUpdateData, TaskCreateData


class TaskService:
    def __init__(self, task_repo: ITaskRepository):
        self.task_repo = task_repo

    async def get_task_by_id(self, task_id: UUID) -> Optional[Task]:
        return await self.task_repo.get_by_id(task_id)

    async def get_all_tasks(self) -> List[Task]:
        return await self.task_repo.get_all()

    async def create_task(self, task_data: TaskCreateData) -> Task:
        return await self.task_repo.create(task_data)

    async def update_task(self, task_id: UUID, task_data: TaskUpdateData) -> Optional[Task]:
        return await self.task_repo.update(task_id, task_data)

    async def delete_task(self, task_id: UUID) -> bool:
        return await self.task_repo.delete(task_id)
