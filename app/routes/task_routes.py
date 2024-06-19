import datetime
import os
from flask import Blueprint, abort, make_response, request, Response
from ..db import db
from ..models.task import Task
import requests
from .helpers import serialize_with
from .task_helpers import require_task
from ..serializers.one_task import OneTask
from ..serializers.empty_body import EmptyBody
from ..serializers.list_of_tasks import ListOfTasks

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
@serialize_with(ListOfTasks())
def task_index():
    sort_dir = request.args.get("sort")

    if sort_dir == "asc":
        query = db.select(Task).order_by(Task.title)
    elif sort_dir == "desc":
        query = db.select(Task).order_by(Task.title.desc())
    else:
        query = db.select(Task)

    tasks = db.session.scalars(query)

    return tasks

@bp.get("/<task_id>")
@require_task
@serialize_with(OneTask())
def get_one_task(task):
    return task

@bp.post("")
@serialize_with(OneTask(), 201)
def create_task():
    data = request.get_json()

    try:
        task = Task.from_dict(data)
    except KeyError:
        abort(make_response(dict(details="Invalid data"), 400))

    db.session.add(task)
    db.session.commit()

    return task

@bp.put("/<task_id>")
@require_task
@serialize_with(OneTask())
def update_task(task):
    data = request.get_json()

    try:
        task.title = data["title"]
        task.description = data["description"]
    except KeyError:
        abort(make_response(dict(details="Invalid data"), 400))

    db.session.commit()

    return task

@bp.delete("/<task_id>")
@require_task
@serialize_with(EmptyBody(), 204)
def delete_task(task):
    db.session.delete(task)
    db.session.commit()

@bp.patch("/<task_id>/mark_complete")
@require_task
@serialize_with(OneTask())
def mark_complete(task):
    task.completed_at = datetime.datetime.now(datetime.timezone.utc)

    db.session.commit()

    notify_complete(task)

    return task

@bp.patch("/<task_id>/mark_incomplete")
@require_task
@serialize_with(OneTask())
def mark_incomplete(task):
    task.completed_at = None

    db.session.commit()

    return task
