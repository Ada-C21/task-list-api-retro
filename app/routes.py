import datetime
import os
from flask import Blueprint, abort, make_response, request
from app import db
from .models.task import Task
from .models.goal import Goal
import requests

SLACK_API_URL = "https://slack.com/api/chat.postMessage"
SLACK_BOT_TOKEN = os.environ.get("SLACK_BOT_TOKEN")

task_bp = Blueprint("task", __name__, url_prefix="/tasks")
goal_bp = Blueprint("goal", __name__, url_prefix="/goals")

def notify_complete(task):
    if not SLACK_BOT_TOKEN:
        return
    
    headers = {
        "Authorization": f"Bearer {SLACK_BOT_TOKEN}",
    }

    data = {
        "channel": "task-notifications-demo",
        "text": f'Task "{task.title}" has been marked complete',
    }

    requests.post(SLACK_API_URL, headers=headers, data=data)

@task_bp.get("")
def task_index():
    sort_dir = request.args.get("sort")

    if sort_dir == "asc":
        query = db.select(Task).order_by(Task.title)
    elif sort_dir == "desc":
        query = db.select(Task).order_by(Task.title.desc())
    else:
        query = db.select(Task)

    tasks = db.session.scalars(query)

    return [task.to_dict() for task in tasks]

@task_bp.get("/<task_id>")
def get_one_task(task_id):
    query = db.select(Task).where(Task.task_id == task_id)
    task = db.session.scalar(query)

    if not task:
        abort(make_response(dict(
            details=f"Unknown Task id: {task_id}"
        ), 404))

    return dict(task=task.to_dict())

@task_bp.post("")
def create_task():
    data = request.get_json()

    try:
        task = Task.from_dict(data)
    except KeyError:
        abort(make_response(dict(details="Invalid data"), 400))

    db.session.add(task)
    db.session.commit()

    return dict(task=task.to_dict()), 201

@task_bp.put("/<task_id>")
def update_task(task_id):
    data = request.get_json()
    query = db.select(Task).where(Task.task_id == task_id)
    task = db.session.scalar(query)

    if not task:
        abort(make_response(dict(
            details=f"Unknown Task id: {task_id}"
        ), 404))

    try:
        task.title = data["title"]
        task.description = data["description"]
    except KeyError:
        abort(make_response(dict(details="Invalid data"), 400))

    db.session.commit()

    return dict(task=task.to_dict())

@task_bp.delete("/<task_id>")
def delete_task(task_id):
    query = db.select(Task).where(Task.task_id == task_id)
    task = db.session.scalar(query)

    if not task:
        abort(make_response(dict(
            details=f"Unknown Task id: {task_id}"
        ), 404))

    db.session.delete(task)
    db.session.commit()

    return dict(details=f'Task {task.task_id} "{task.title}" successfully deleted')

@task_bp.patch("/<task_id>/mark_complete")
def mark_complete(task_id):
    query = db.select(Task).where(Task.task_id == task_id)
    task = db.session.scalar(query)

    if not task:
        abort(make_response(dict(
            details=f"Unknown Task id: {task_id}"
        ), 404))

    task.completed_at = datetime.datetime.now(datetime.timezone.utc)

    db.session.commit()

    notify_complete(task)

    return dict(task=task.to_dict())

@task_bp.patch("/<task_id>/mark_incomplete")
def mark_incomplete(task_id):
    query = db.select(Task).where(Task.task_id == task_id)
    task = db.session.scalar(query)

    if not task:
        abort(make_response(dict(
            details=f"Unknown Task id: {task_id}"
        ), 404))

    task.completed_at = None

    db.session.commit()

    return dict(task=task.to_dict())

@goal_bp.get("")
def goal_index():
    query = db.select(Goal)
    goals = db.session.scalars(query)

    return [goal.to_dict() for goal in goals]

@goal_bp.get("/<goal_id>")
def get_one_goal(goal_id):
    query = db.select(Goal).where(Goal.goal_id == goal_id)
    goal = db.session.scalar(query)

    if not goal:
        abort(make_response(dict(
            details=f"Unknown Goal id: {goal_id}"
        ), 404))

    return dict(goal=goal.to_dict())

@goal_bp.post("")
def create_goal():
    data = request.get_json()

    try:
        goal = Goal.from_dict(data)
    except KeyError:
        abort(make_response(dict(details="Invalid data"), 400))

    db.session.add(goal)
    db.session.commit()

    return dict(goal=goal.to_dict()), 201

@goal_bp.put("/<goal_id>")
def update_goal(goal_id):
    data = request.get_json()
    query = db.select(Goal).where(Goal.goal_id == goal_id)
    goal = db.session.scalar(query)

    if not goal:
        abort(make_response(dict(
            details=f"Unknown Goal id: {goal_id}"
        ), 404))

    try:
        goal.title = data["title"]
    except KeyError:
        abort(make_response(dict(details="Invalid data"), 400))

    db.session.commit()

    return dict(goal=goal.to_dict())

@goal_bp.delete("/<goal_id>")
def delete_goal(goal_id):
    query = db.select(Goal).where(Goal.goal_id == goal_id)
    goal = db.session.scalar(query)

    if not goal:
        abort(make_response(dict(
            details=f"Unknown Goal id: {goal_id}"
        ), 404))

    db.session.delete(goal)
    db.session.commit()

    return dict(details=f'Goal {goal.goal_id} "{goal.title}" successfully deleted')

@goal_bp.post("/<goal_id>/tasks")
def set_goal_tasks(goal_id):
    data = request.get_json()
    query = db.select(Goal).where(Goal.goal_id == goal_id)
    goal = db.session.scalar(query)

    if not goal:
        abort(make_response(dict(
            details=f"Unknown Goal id: {goal_id}"
        ), 404))

    try:
        task_ids = data["task_ids"]
        tasks = []
        for task_id in task_ids:
            query = db.select(Task).where(Task.task_id == task_id)
            task = db.session.scalar(query)
            if not task:
                abort(make_response(dict(details=f"Unknown Task id: {task_id}"), 404))
            tasks.append(task)

        goal.tasks = tasks
    except KeyError:
        abort(make_response(dict(details="Invalid data"), 400))

    db.session.commit()

    return dict(id=goal.goal_id, task_ids=[task.task_id for task in tasks])

@goal_bp.get("/<goal_id>/tasks")
def get_goal_tasks(goal_id):
    query = db.select(Goal).where(Goal.goal_id == goal_id)
    goal = db.session.scalar(query)

    if not goal:
        abort(make_response(dict(
            details=f"Unknown Goal id: {goal_id}"
        ), 404))

    response = goal.to_dict()
    tasks = goal.tasks
    response["tasks"] = [task.to_dict() for task in tasks]

    return response
