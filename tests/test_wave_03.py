import unittest
from unittest.mock import Mock, patch
from datetime import datetime
from app.models.task import Task
from app import db
import pytest


def test_mark_complete_on_incomplete_task(client, one_task, one_session):
    # Arrange
    """
    The future Wave 4 adds special functionality to this route,
    so for this test, we need to set-up "mocking."

    Mocking will help our tests work in isolation, which is a
    good thing!

    We need to mock any POST requests that may occur during this
    test (due to Wave 4).

    There is no action needed here, the tests should work as-is.
    """
    with patch("requests.post") as mock_get:
        mock_get.return_value.status_code = 200

        # Act
        client.set_cookie("SessionID", str(one_session.id))
        response = client.patch("/tasks/1/mark_complete")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert "task" in response_body
    assert response_body["task"]["is_complete"] == True
    assert response_body == {
        "task": {
            "id": 1,
            "title": "Go on my daily walk 🏞",
            "description": "Notice something new every day",
            "is_complete": True
        }
    }
    assert db.session.scalar(db.select(Task).where(Task.id == 1)).completed_at


def test_mark_incomplete_on_complete_task(client, completed_task, one_session):
    # Act
    client.set_cookie("SessionID", str(one_session.id))
    response = client.patch("/tasks/1/mark_incomplete")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body["task"]["is_complete"] == False
    assert response_body == {
        "task": {
            "id": 1,
            "title": "Go on my daily walk 🏞",
            "description": "Notice something new every day",
            "is_complete": False
        }
    }
    assert db.session.scalar(db.select(Task).where(Task.id == 1)).completed_at == None


def test_mark_complete_on_completed_task(client, completed_task, one_session):
    # Arrange
    """
    The future Wave 4 adds special functionality to this route,
    so for this test, we need to set-up "mocking."

    Mocking will help our tests work in isolation, which is a
    good thing!

    We need to mock any POST requests that may occur during this
    test (due to Wave 4).

    There is no action needed here, the tests should work as-is.
    """
    with patch("requests.post") as mock_get:
        mock_get.return_value.status_code = 200

        # Act
        client.set_cookie("SessionID", str(one_session.id))
        response = client.patch("/tasks/1/mark_complete")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert "task" in response_body
    assert response_body["task"]["is_complete"] == True
    assert response_body == {
        "task": {
            "id": 1,
            "title": "Go on my daily walk 🏞",
            "description": "Notice something new every day",
            "is_complete": True
        }
    }
    assert db.session.scalar(db.select(Task).where(Task.id == 1)).completed_at


def test_mark_incomplete_on_incomplete_task(client, one_task, one_session):
    # Act
    client.set_cookie("SessionID", str(one_session.id))
    response = client.patch("/tasks/1/mark_incomplete")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body["task"]["is_complete"] == False
    assert response_body == {
        "task": {
            "id": 1,
            "title": "Go on my daily walk 🏞",
            "description": "Notice something new every day",
            "is_complete": False
        }
    }
    assert db.session.scalar(db.select(Task).where(Task.id == 1)).completed_at == None


def test_mark_complete_missing_task(client, one_session):
    # Act
    client.set_cookie("SessionID", str(one_session.id))
    response = client.patch("/tasks/1/mark_complete")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 404
    assert response_body == dict(details="Unknown Task id: 1")


def test_mark_incomplete_missing_task(client, one_session):
    # Act
    client.set_cookie("SessionID", str(one_session.id))
    response = client.patch("/tasks/1/mark_incomplete")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 404
    assert response_body == dict(details="Unknown Task id: 1")
