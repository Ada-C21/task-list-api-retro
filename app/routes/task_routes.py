import datetime
import os
from flask import Blueprint, abort, make_response, request, Response
from ..db import db
from ..models.task import Task
import requests
from .helpers import validate_model
from functools import wraps

SLACK_API_URL = "https://slack.com/api/chat.postMessage"
SLACK_BOT_TOKEN = os.environ.get("SLACK_BOT_TOKEN")

bp = Blueprint("task", __name__, url_prefix="/tasks")

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

@bp.get("")
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

# incomplete livecode decorator version
# def require_task(fn):
#     def wrapper(task_id):
#         task = validate_model(Task, task_id)
#         return fn(task=task)

#     return wrapper

# more robust decorator (uses wraps and variadic params)
def require_task(fn):
    @wraps(fn)
    def wrapper(*args, task_id, **kwargs):
        task = validate_model(Task, task_id)
        return fn(*args, task=task, **kwargs)

    return wrapper


@bp.get("/<task_id>")
@require_task
def get_one_task(task):
    return dict(task=task.to_dict())

@bp.post("")
def create_task():
    data = request.get_json()

    try:
        task = Task.from_dict(data)
    except KeyError:
        abort(make_response(dict(details="Invalid data"), 400))

    db.session.add(task)
    db.session.commit()

    return dict(task=task.to_dict()), 201

@bp.put("/<task_id>")
@require_task
def update_task(task):
    data = request.get_json()

    try:
        task.title = data["title"]
        task.description = data["description"]
    except KeyError:
        abort(make_response(dict(details="Invalid data"), 400))

    db.session.commit()

    return dict(task=task.to_dict())

@bp.delete("/<task_id>")
@require_task
def delete_task(task):
    db.session.delete(task)
    db.session.commit()

    return Response(status=204, mimetype="application/json")

@bp.patch("/<task_id>/mark_complete")
@require_task
def mark_complete(task):
    task.completed_at = datetime.datetime.now(datetime.timezone.utc)

    db.session.commit()

    notify_complete(task)

    return dict(task=task.to_dict())

@bp.patch("/<task_id>/mark_incomplete")
@require_task
def mark_incomplete(task):
    task.completed_at = None

    db.session.commit()

    return dict(task=task.to_dict())
