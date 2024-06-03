import datetime
from flask import Blueprint, jsonify, abort, make_response, request
from app import db
from .models.task import Task
from .models.goal import Goal

task_bp = Blueprint("task", __name__, url_prefix="/tasks")
goal_bp = Blueprint("goal", __name__, url_prefix="/goals")

@task_bp.route("", methods=["GET"])
def task_index():
    sort_dir = request.args.get("sort")

    if sort_dir == "asc":
        tasks = Task.query.order_by(Task.title).all()
    elif sort_dir == "desc":
        tasks = Task.query.order_by(Task.title.desc()).all()
    else:
        tasks = Task.query.all()

    return jsonify([task.to_dict() for task in tasks])

@task_bp.route("/<task_id>", methods=["GET"])
def get_one_task(task_id):
    task = Task.query.get(task_id)

    if not task:
        abort(make_response(dict(
            details=f"Unknown Task id: {task_id}"
        ), 404))

    return dict(task=task.to_dict())

@task_bp.route("", methods=["POST"])
def create_task():
    data = request.get_json()

    try:
        task = Task.from_dict(data)
    except KeyError:
        abort(make_response(dict(details="Invalid data"), 400))

    db.session.add(task)
    db.session.commit()

    return dict(task=task.to_dict()), 201

@task_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):
    data = request.get_json()
    task = Task.query.get(task_id)

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

@task_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = Task.query.get(task_id)

    if not task:
        abort(make_response(dict(
            details=f"Unknown Task id: {task_id}"
        ), 404))

    db.session.delete(task)
    db.session.commit()

    return dict(details=f'Task {task.task_id} "{task.title}" successfully deleted')

@task_bp.route("/<task_id>/mark_complete", methods=["PATCH"])
def mark_complete(task_id):
    task = Task.query.get(task_id)

    if not task:
        abort(make_response(dict(
            details=f"Unknown Task id: {task_id}"
        ), 404))

    task.completed_at = datetime.datetime.now(datetime.timezone.utc)

    db.session.commit()

    return dict(task=task.to_dict())

@task_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"])
def mark_incomplete(task_id):
    task = Task.query.get(task_id)

    if not task:
        abort(make_response(dict(
            details=f"Unknown Task id: {task_id}"
        ), 404))

    task.completed_at = None

    db.session.commit()

    return dict(task=task.to_dict())

@goal_bp.route("", methods=["GET"])
def goal_index():
    goals = Goal.query.all()

    return jsonify([goal.to_dict() for goal in goals])

@goal_bp.route("/<goal_id>", methods=["GET"])
def get_one_goal(goal_id):
    goal = Goal.query.get(goal_id)

    if not goal:
        abort(make_response(dict(
            details=f"Unknown Goal id: {goal_id}"
        ), 404))

    return dict(goal=goal.to_dict())

@goal_bp.route("", methods=["POST"])
def create_goal():
    data = request.get_json()

    try:
        goal = Goal.from_dict(data)
    except KeyError:
        abort(make_response(dict(details="Invalid data"), 400))

    db.session.add(goal)
    db.session.commit()

    return dict(goal=goal.to_dict()), 201

@goal_bp.route("/<goal_id>", methods=["PUT"])
def update_goal(goal_id):
    data = request.get_json()
    goal = Goal.query.get(goal_id)

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

@goal_bp.route("/<goal_id>", methods=["DELETE"])
def delete_goal(goal_id):
    goal = Goal.query.get(goal_id)

    if not goal:
        abort(make_response(dict(
            details=f"Unknown Goal id: {goal_id}"
        ), 404))

    db.session.delete(goal)
    db.session.commit()

    return dict(details=f'Goal {goal.goal_id} "{goal.title}" successfully deleted')

@goal_bp.route("/<goal_id>/tasks", methods=["POST"])
def set_goal_tasks(goal_id):
    data = request.get_json()
    goal = Goal.query.get(goal_id)

    if not goal:
        abort(make_response(dict(
            details=f"Unknown Goal id: {goal_id}"
        ), 404))

    try:
        task_ids = data["task_ids"]
        tasks = []
        for task_id in task_ids:
            task = Task.query.get(task_id)
            if not task:
                abort(make_response(dict(details=f"Unknown Task id: {task_id}"), 404))
            tasks.append(task)

        goal.tasks = tasks
    except KeyError:
        abort(make_response(dict(details="Invalid data"), 400))

    db.session.commit()

    return dict(id=goal.goal_id, task_ids=[task.task_id for task in tasks])

@goal_bp.route("/<goal_id>/tasks", methods=["GET"])
def get_goal_tasks(goal_id):
    goal = Goal.query.get(goal_id)

    if not goal:
        abort(make_response(dict(
            details=f"Unknown Goal id: {goal_id}"
        ), 404))

    response = goal.to_dict()
    tasks = goal.tasks
    response["tasks"] = [task.to_dict() for task in tasks]

    return response
