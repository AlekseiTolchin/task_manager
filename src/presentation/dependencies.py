from fastapi import Depends

from src.application.services.task_service import TaskService
from src.infrastructure.database.dependencies import get_task_service_impl


def get_task_service(service: TaskService = Depends(get_task_service_impl)) -> TaskService:
    return service
