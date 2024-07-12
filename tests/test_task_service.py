import pytest
from app.services.task_service import TaskService
from app.errors.invalid_request_data_error import InvalidRequestDataError
from app.errors.record_not_found_error import RecordNotFoundError
from app.models.task import Task
from sqlalchemy import ScalarResult

def test_get_tasks_no_saved_tasks(test_db):
    # Arrange
    task_service = TaskService(test_db)

    # Act
    result = task_service.get_tasks()
    result_list = list(result)

    # Assert
    assert type(result) == ScalarResult
    assert result_list == []


def test_get_tasks_one_saved_tasks(test_db, one_task):
    # Arrange
    task_service = TaskService(test_db)

    # Act
    result = task_service.get_tasks()
    result_list = list(result)

    # Assert
    assert type(result) == ScalarResult
    assert len(result_list) == 1
    assert result_list[0].id == 1
    assert result_list[0].title == "Go on my daily walk 🏞"
    assert result_list[0].description == "Notice something new every day"
    assert result_list[0].is_complete() == False


def test_create_task(test_db):
    # Arrange
    task_service = TaskService(test_db)
    data = {
        "title": "A Brand New Task",
        "description": "Test Description",
    }

    # Act
    result = task_service.create_task(data)

    # Assert
    assert result.id == 1
    assert result.title == "A Brand New Task"
    assert result.description == "Test Description"
    assert result.is_complete() == False
    assert len(list(task_service.get_tasks())) == 1


def test_create_task_must_contain_title(test_db):
    # Arrange
    task_service = TaskService(test_db)
    data = {
        "description": "Test Description",
    }

    # Act
    with pytest.raises(InvalidRequestDataError):
        task_service.create_task(data)

    # Assert
    assert len(list(task_service.get_tasks())) == 0


def test_create_task_must_contain_description(test_db):
    # Arrange
    task_service = TaskService(test_db)
    data = {
        "title": "A Brand New Task",
    }

    # Act
    with pytest.raises(InvalidRequestDataError):
        task_service.create_task(data)

    # Assert
    assert len(list(task_service.get_tasks())) == 0


def test_update_task(test_db, one_task):
    # Arrange
    task_service = TaskService(test_db)
    data = {
        "title": "Updated Task Title",
        "description": "Updated Test Description",
    }

    # Act
    result = task_service.update_task(one_task, data)
    fetched_task = Task.get_by_id(one_task.id)

    # Assert
    assert len(list(task_service.get_tasks())) == 1
    assert result.title == "Updated Task Title"
    assert result.description == "Updated Test Description"
    assert result.completed_at == None
    assert fetched_task.title == "Updated Task Title"
    assert fetched_task.description == "Updated Test Description"
    assert fetched_task.completed_at == None


def test_update_task_not_found(test_db):
    # Arrange
    task_service = TaskService(test_db)
    fake_task = Task(id=1, title="Fake Task", description="Fake Description")
    data = {
        "title": "Updated Task Title",
        "description": "Updated Test Description",
    }

    # Act
    # Doesn't cause any errors since since the local data can still be updated
    # The internal commit essentially does nothing in this case
    task_service.update_task(fake_task, data)

    # Assert
    # The fake model shouldn't have been added to the database
    assert len(list(task_service.get_tasks())) == 0


def test_delete_task(test_db, one_task):
    # Arrange
    task_service = TaskService(test_db)

    # Act
    task_service.delete_task(one_task)

    # Assert
    assert len(list(task_service.get_tasks())) == 0


def test_delete_task_not_found(test_db):
    # Arrange
    task_service = TaskService(test_db)
    fake_task = Task(id=1, title="Fake Task", description="Fake Description")

    # Act
    with pytest.raises(RecordNotFoundError):
        task_service.delete_task(fake_task)

    # Assert
    assert len(list(task_service.get_tasks())) == 0
