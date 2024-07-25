from flask import Blueprint, request, g
from ..db import db
from .helpers import serialize_with, handle_invalid_data
from .task_helpers import require_task
from .session_helpers import require_auth
from ..serializers.one_task import OneTask
from ..serializers.empty_body import EmptyBody
from ..serializers.list_of_tasks import ListOfTasks
from ..services.task_service import TaskService

bp = Blueprint("task", __name__, url_prefix="/tasks")

@bp.get("")
@require_auth(db)
@serialize_with(ListOfTasks())
def task_index():
    return TaskService(db).get_tasks(sort_dir=request.args.get("sort"), user=g.user)

@bp.get("/<task_id>")
@require_auth(db)
@require_task
@serialize_with(OneTask())
def get_one_task(task):
    return task

@bp.post("")
@require_auth(db)
@serialize_with(OneTask(), 201)
@handle_invalid_data
def create_task():
    return TaskService(db).create_task(request.get_json(), user=g.user)

@bp.put("/<task_id>")
@require_auth(db)
@require_task
@serialize_with(OneTask())
@handle_invalid_data
def update_task(task):
    return TaskService(db).update_task(task, request.get_json(), user=g.user)

@bp.delete("/<task_id>")
@require_auth(db)
@require_task
@serialize_with(EmptyBody(), 204)
def delete_task(task):
    return TaskService(db).delete_task(task, user=g.user)

@bp.patch("/<task_id>/mark_complete")
@require_auth(db)
@require_task
@serialize_with(OneTask())
def mark_complete(task):
    return TaskService(db).mark_complete(task, user=g.user)

@bp.patch("/<task_id>/mark_incomplete")
@require_auth(db)
@require_task
@serialize_with(OneTask())
def mark_incomplete(task):
    return TaskService(db).mark_incomplete(task, user=g.user)
