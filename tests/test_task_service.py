from uuid import UUID

from src.domain.models.tasks import Task
from src.domain.repositories.tasks import TaskCreateData, TaskUpdateData
from src.application.services.task_service import TaskService


async def test_get_task_by_id_found(mock_repo):
    """Получение задачи по ID через сервис."""
    mock_task = Task(
        id=UUID('3fa85f64-5717-4562-b3fc-2c963f66afa6'),
        title='A',
        description='B',
        status='CREATED',
        created_at=None,
        updated_at=None,
    )
    mock_repo.get_by_id.return_value = mock_task
    service = TaskService(task_repo=mock_repo)
    result = await service.get_task_by_id(mock_task.id)
    assert result == mock_task
    mock_repo.get_by_id.assert_awaited_once_with(mock_task.id)


async def test_create_task(mock_repo):
    """Создание задачи через сервис."""
    create_data = TaskCreateData(title='T', description='D')
    mock_task = Task(
        id=UUID("3fa85f64-5717-4562-b3fc-2c963f66afa6"),
        title='T',
        description='D',
        status='CREATED',
        created_at=None,
        updated_at=None,
    )
    mock_repo.create.return_value = mock_task
    service = TaskService(task_repo=mock_repo)
    result = await service.create_task(create_data)
    assert result == mock_task
    mock_repo.create.assert_awaited_once_with(create_data)


async def test_update_task_found(mock_repo):
    """Обновление задачи через сервис."""
    update_data = TaskUpdateData(title='T2', description='D2', status='в работе')
    task_id = UUID("3fa85f64-5717-4562-b3fc-2c963f66afa6")
    mock_task = Task(
        id=task_id,
        title='T2',
        description='D2',
        status='в работе',
        created_at=None,
        updated_at=None,
    )
    mock_repo.update.return_value = mock_task
    service = TaskService(task_repo=mock_repo)
    result = await service.update_task(task_id, update_data)
    assert result == mock_task
    mock_repo.update.assert_awaited_once_with(task_id, update_data)


async def test_delete_task_success(mock_repo):
    """Удаление задачи через сервис."""
    task_id = UUID('3fa85f64-5717-4562-b3fc-2c963f66afa6')
    mock_repo.delete.return_value = True
    service = TaskService(task_repo=mock_repo)
    result = await service.delete_task(task_id)
    assert result is True
    mock_repo.delete.assert_awaited_once_with(task_id)
