from flask import Blueprint, abort, make_response, request, Response
from ..db import db
from ..models.task import Task
from ..models.goal import Goal
from .helpers import validate_model
from functools import wraps

bp = Blueprint("goal", __name__, url_prefix="/goals")

@bp.get("")
def goal_index():
    query = db.select(Goal)
    goals = db.session.scalars(query)

    return [goal.to_dict() for goal in goals]

# more robust decorator (uses wraps and variadic params)
def require_goal(fn):
    @wraps(fn)
    def wrapper(*args, goal_id, **kwargs):
        goal = validate_model(Goal, goal_id)
        return fn(*args, goal=goal, **kwargs)

    return wrapper

@bp.get("/<goal_id>")
@require_goal
def get_one_goal(goal):
    return dict(goal=goal.to_dict())

@bp.post("")
def create_goal():
    data = request.get_json()

    try:
        goal = Goal.from_dict(data)
    except KeyError:
        abort(make_response(dict(details="Invalid data"), 400))

    db.session.add(goal)
    db.session.commit()

    return dict(goal=goal.to_dict()), 201

@bp.put("/<goal_id>")
@require_goal
def update_goal(goal):
    data = request.get_json()

    try:
        goal.title = data["title"]
    except KeyError:
        abort(make_response(dict(details="Invalid data"), 400))

    db.session.commit()

    return dict(goal=goal.to_dict())

@bp.delete("/<goal_id>")
@require_goal
def delete_goal(goal):
    db.session.delete(goal)
    db.session.commit()

    return Response(status=204, mimetype="application/json")

@bp.post("/<goal_id>/tasks")
@require_goal
def set_goal_tasks(goal):
    data = request.get_json()

    try:
        task_ids = data["task_ids"]
        tasks = []
        for task_id in task_ids:
            query = db.select(Task).where(Task.id == task_id)
            task = db.session.scalar(query)
            if not task:
                abort(make_response(dict(details=f"Unknown Task id: {task_id}"), 404))
            tasks.append(task)

        goal.tasks = tasks
    except KeyError:
        abort(make_response(dict(details="Invalid data"), 400))

    db.session.commit()

    return dict(id=goal.id, task_ids=[task.id for task in tasks])

@bp.get("/<goal_id>/tasks")
@require_goal
def get_goal_tasks(goal):
    response = goal.to_dict()
    tasks = goal.tasks
    response["tasks"] = [task.to_dict() for task in tasks]

    return response
