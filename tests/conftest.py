import pytest
from unittest import mock
from app import create_app
from app.models.task import Task
from app.models.goal import Goal
from app.models.user import User
from app.models.session import Session
from app.db import db
from app.bcrypt import bcrypt
import datetime
from flask.signals import request_finished
import os
from app.services import session_service
from app.util import time

# writing tests that involve datetime checks can be tricky
# one package we can investigate is called freezegun
# we're going to do pretty hacky stuff here just to get the tests to work

TEST_NOW = datetime.datetime(2021, 9, 1, 0, 0, 0, 0, datetime.timezone.utc)
SESSION_MINUTES = 30

@pytest.fixture
def app():
    # create the app with a test config dictionary
    app = create_app({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": os.environ.get(
            "SQLALCHEMY_TEST_DATABASE_URI")
        })

    @request_finished.connect_via(app)
    def expire_session(sender, response, **extra):
        db.session.remove()

    with app.app_context():
        db.create_all()
        yield app

    # close and remove the temporary database
    with app.app_context():
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def one_user(app):
    name = "u1"
    email = "e1"
    password = "p"
    pwd_hash = bcrypt.generate_password_hash(password).decode("utf-8")
    user = User(name=name, email=email, pwd_hash=pwd_hash)

    db.session.add(user)
    db.session.commit()
    return user

@pytest.fixture
def override_now(monkeypatch):
    with mock.patch('app.util.time.now', return_value=TEST_NOW):
        yield


@pytest.fixture
def one_session(app, one_user, override_now):
    expires_at = TEST_NOW + datetime.timedelta(minutes=SESSION_MINUTES)
    session = Session(user_id=one_user.id, expires_at=expires_at)

    db.session.add(session)
    db.session.commit()

    return session

# This fixture gets called in every test that
# references "one_task"
# This fixture creates a task and saves it in the database
@pytest.fixture
def one_task(one_user):
    new_task = Task(
        title="Go on my daily walk 🏞", 
        description="Notice something new every day", 
        completed_at=None, 
        user_id=one_user.id)
    db.session.add(new_task)
    db.session.commit()
    return new_task


# This fixture gets called in every test that
# references "three_tasks"
# This fixture creates three tasks and saves
# them in the database
@pytest.fixture
def three_tasks(one_user):
    tasks = [
        Task(
            title="Water the garden 🌷", description="", completed_at=None, user_id=one_user.id),
        Task(
            title="Answer forgotten email 📧", description="", completed_at=None, user_id=one_user.id),
        Task(
            title="Pay my outstanding tickets 😭", description="", completed_at=None, user_id=one_user.id)
    ]
    db.session.add_all(tasks)
    db.session.commit()
    return tasks


# This fixture gets called in every test that
# references "completed_task"
# This fixture creates a task with a
# valid completed_at date
@pytest.fixture
def completed_task(one_user):
    completed_at = time.now(datetime.timezone.utc)
    new_task = Task(
        title="Go on my daily walk 🏞", 
        description="Notice something new every day", 
        completed_at=completed_at, 
        user_id=one_user.id)
    db.session.add(new_task)
    db.session.commit()
    return completed_task


# This fixture gets called in every test that
# references "one_goal"
# This fixture creates a goal and saves it in the database
@pytest.fixture
def one_goal(app):
    new_goal = Goal(title="Build a habit of going outside daily")
    db.session.add(new_goal)
    db.session.commit()
    return new_goal


# This fixture gets called in every test that
# references "one_task_belongs_to_one_goal"
# This fixture creates a task and a goal
# It associates the goal and task, so that the
# goal has this task, and the task belongs to one goal
@pytest.fixture
def one_task_belongs_to_one_goal(app, one_goal, one_task):
    task = Task.query.first()
    goal = Goal.query.first()
    goal.tasks.append(task)
    db.session.commit()
    return goal


@pytest.fixture
def test_db(app):
    return db