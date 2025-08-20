from typing import Annotated, List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, status, HTTPException

from src.application.schemas.task import TaskCreate, TaskUpdate, TaskResponse
from src.application.services.task_service import TaskService
from src.domain.repositories.tasks import TaskCreateData, TaskUpdateData
from src.presentation.dependencies import get_task_service

router = APIRouter(
    prefix='/api/tasks',
    tags=['tasks']
)


@router.get('/', response_model=List[TaskResponse])
async def get_tasks(service: Annotated[TaskService, Depends(get_task_service)]):
    tasks = await service.get_all_tasks()
    return [TaskResponse.model_validate(task) for task in tasks]


@router.get('/{task_id}', response_model=TaskResponse)
async def get_task(
        task_id: UUID,
        service: Annotated[TaskService, Depends(get_task_service)]
):
    task = await service.get_task_by_id(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail='Task not found')
    return TaskResponse.model_validate(task)


@router.post('/', response_model=TaskResponse, status_code=201)
async def create_task(
        task: Annotated[TaskCreate, Depends()],
        service: Annotated[TaskService, Depends(get_task_service)]
):
    task_data = TaskCreateData(title=task.title, description=task.description)
    new_task = await service.create_task(task_data)
    return TaskResponse.model_validate(new_task)


@router.put('/{task_id}', response_model=TaskResponse)
async def update_task(
        task_id: UUID,
        task: Annotated[TaskUpdate, Depends()],
        service: Annotated[TaskService, Depends(get_task_service)]
):
    task_data = TaskUpdateData(
        title=task.title,
        description=task.description,
        status=task.status
    )
    updated_task = await service.update_task(task_id, task_data)
    if updated_task is None:
        raise HTTPException(status_code=404, detail='Task not found')
    return TaskResponse.model_validate(updated_task)


@router.delete('/{task_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
        task_id: UUID,
        service: Annotated[TaskService, Depends(get_task_service)]
):
    success = await service.delete_task(task_id)
    if not success:
        raise HTTPException(status_code=404, detail='Task not found')
