from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID, uuid4
from typing import Optional

from src.domain.enums.task_status import TaskStatus


@dataclass
class Task:
    title: str
    id: UUID = field(default_factory=uuid4)
    description: Optional[str] = None
    status: TaskStatus = TaskStatus.CREATED
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
