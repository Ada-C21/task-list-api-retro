import pytest
from app.routes.task_helpers import require_task
from app.routes.helpers import serialize_with
from app.serializers.one_task import OneTask
from werkzeug.exceptions import HTTPException
from flask import g

def test_require_task_with_one_task(one_task, one_session):
    # Arrange
    @require_task
    def mock_route(task):
        return task
    
    # Act
    g.user = one_session.user
    result = mock_route(task_id=1)

    # Assert
    assert result.id == 1
    assert result.title == "Go on my daily walk 🏞"
    assert result.description == "Notice something new every day"
    assert result.is_complete() == False

def test_require_task_with_no_task(one_session):
    # Arrange
    @require_task
    def mock_route(task):
        return task
    
    # Act
    with pytest.raises(HTTPException) as exc_info:
        g.user = one_session.user
        result = mock_route(task_id=1)

    # Assert
    assert exc_info.type == HTTPException
    ex = exc_info.value
    response = ex.get_response()
    assert response.status_code == 404
    assert response.get_json() == dict(details="Unknown Task id: 1")

def test_serialize_with_one_task(one_task):
    @serialize_with(OneTask())
    def mock_route():
        return one_task

    response = mock_route()
    result = response.get_json()
    status = response.status_code
    assert result == {
        "task": {
            "id": 1,
            "title": "Go on my daily walk 🏞",
            "description": "Notice something new every day",
            "is_complete": False
        }
    }

    assert status == 200

def test_serialize_with_no_task(app):
    @serialize_with(OneTask())
    def mock_route():
        return None

    with pytest.raises(AttributeError):
        mock_route()

    # This test documents the behavior of what `serialize_with` will do if
    # the route handler returns None.
    # We don't actually want this behavior in production code, so any route
    # decorated with `serialize_with` should always return a value.
    # If the route would return None for some reason (such as not finding a
    # record in the database), then the route should raise an exception
    # (e.g. RecordNotFoundError) and this should be caught by error
    # handling logic and turned into a proper HTTP response (with `abort`).
    # This test is here to document the behavior and to ensure that we don't
    # unnecessarily change it.

# Tests for other decorators can be added here
