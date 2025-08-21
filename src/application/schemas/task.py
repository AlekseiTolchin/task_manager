from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from src.domain.enums.task_status import TaskStatus


class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    status: Optional[TaskStatus] = None


class TaskCreate(TaskBase):
    pass


class TaskUpdate(TaskBase):
    pass


class TaskResponse(TaskBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
