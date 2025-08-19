from abc import ABC, abstractmethod
from dataclasses import dataclass
from uuid import UUID
from typing import List, Optional

from src.domain.models.tasks import Task
from src.domain.enums.task_status import TaskStatus


@dataclass
class TaskCreateData:
    title: str
    description: str


@dataclass
class TaskUpdateData:
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[TaskStatus] = None


class ITaskRepository(ABC):
    @abstractmethod
    async def create(self, task_data: TaskCreateData) -> Task:
        pass

    @abstractmethod
    async def get_by_id(self, task_id: UUID) -> Optional[Task]:
        pass

    @abstractmethod
    async def get_all(self) -> List[Task]:
        pass

    @abstractmethod
    async def update(self, task_id: UUID, task_data: TaskUpdateData) -> Optional[Task]:
        pass

    @abstractmethod
    async def delete(self, task_id: UUID) -> bool:
        pass
