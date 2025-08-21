import asyncio


async def test_create_and_get_task(client):
    """Тест создания задачи и получения её по ID."""
    task_payload= {
        'title': 'Test Task',
        'description': 'Test Description'
    }
    create_response = await client.post('/api/tasks/', json=task_payload)
    assert create_response.status_code == 201
    created_task = create_response.json()
    assert created_task['title'] == 'Test Task'
    assert created_task['description'] == 'Test Description'
    assert 'id' in created_task
    assert 'created_at' in created_task
    assert 'updated_at' in created_task

    response = await client.get(f"/api/tasks/{created_task['id']}")
    assert response.status_code == 200
    assert response.json() == created_task


async def test_get_task_not_found(client):
    """Тест получения несуществующей задачи (ожидается 404)."""
    response = await client.get(f'/api/tasks/3fa85f64-5717-4562-b3fc-2c963f66afa6')
    assert response.status_code == 404
    assert response.json()['detail'] == 'Task not found'


async def test_update_task(client):
    """Тест полного обновления задачи."""
    task = {
        'title': 'Task',
        'description': 'Description'
    }
    updated_task_data = {
        'title': 'Updated Task',
        'description': 'Updated Description',
        'status': 'в работе'
    }
    create_response = await client.post('/api/tasks/', json=task)
    assert create_response.status_code == 201
    created = create_response.json()
    await asyncio.sleep(1)

    update_response = await client.put(f"/api/tasks/{created['id']}", json=updated_task_data)
    assert update_response.status_code == 200
    updated = update_response.json()
    assert updated['title'] == 'Updated Task'
    assert updated['description'] == 'Updated Description'
    assert updated['status'] == 'в работе'
    assert updated['created_at'] < updated['updated_at']


async def test_delete_task(client):
    """Тест удаления задачи и последующего получения 404."""
    task = {
        'title': 'Task',
        'description': 'Description'
    }
    create_response = await client.post('/api/tasks/', json=task)
    assert create_response.status_code == 201
    created_task = create_response.json()

    delete_response = await client.delete(f"/api/tasks/{created_task['id']}")
    assert delete_response.status_code == 204

    response = await client.get(f"/api/tasks/{created_task['id']}")
    assert response.status_code == 404
    assert response.json()['detail'] == 'Task not found'


async def test_get_all_tasks(client):
    """Тест получения всех задач."""
    task_1 = {
        'title': 'Task_1',
        'description': 'Description_1'
    }
    task_2 = {
        'title': 'Task_2',
        'description': 'Description_2'
    }
    await client.post('/api/tasks/', json=task_1)
    await client.post('/api/tasks/', json=task_2)

    response = await client.get('/api/tasks/')
    assert response.status_code == 200
    tasks = response.json()
    assert len(tasks) > 1
    assert tasks[0]['title'] == 'Task_1'
    assert tasks[1]['title'] == 'Task_2'


async def test_create_task_invalid_payload(client):
    """Тест создания задачи с невалидными данными (ожидается 422)."""
    task_payload = {'description': 'description only'}
    response = await client.post('/api/tasks/', json=task_payload)
    assert response.status_code == 422


async def test_update_task_invalid_status(client):
    """Тест обновления задачи с невалидным статусом (ожидается 422)."""
    task = {'title': 'Task', 'description': 'Desc'}
    create_response = await client.post('/api/tasks/', json=task)
    assert create_response.status_code == 201
    created_task = create_response.json()
    update_payload = {
        'title': 'Test',
        'description': 'Desc',
        'status': 'неправильный_статус'
    }
    update_response = await client.put(f"/api/tasks/{created_task['id']}", json=update_payload)
    assert update_response.status_code == 422
