from flask import Blueprint, abort, make_response, request, Response
from ..db import db
from ..models.task import Task
from ..models.goal import Goal
from .goal_helpers import require_goal
from .helpers import serialize_with
from ..serializers.one_goal import OneGoal
from ..serializers.list_of_goals import ListOfGoals
from ..serializers.empty_body import EmptyBody
from ..serializers.shallow_goal_with_tasks import ShallowGoalWithTasks
from ..serializers.goal_with_tasks import GoalWithTasks

bp = Blueprint("goal", __name__, url_prefix="/goals")

@bp.get("")
@serialize_with(ListOfGoals())
def goal_index():
    query = db.select(Goal)
    goals = db.session.scalars(query)

    return goals

@bp.get("/<goal_id>")
@require_goal
@serialize_with(OneGoal())
def get_one_goal(goal):
    return goal

@bp.post("")
@serialize_with(OneGoal(), 201)
def create_goal():
    data = request.get_json()

    try:
        goal = Goal.from_dict(data)
    except KeyError:
        abort(make_response(dict(details="Invalid data"), 400))

    db.session.add(goal)
    db.session.commit()

    return goal

@bp.put("/<goal_id>")
@require_goal
@serialize_with(OneGoal())
def update_goal(goal):
    data = request.get_json()

    try:
        goal.title = data["title"]
    except KeyError:
        abort(make_response(dict(details="Invalid data"), 400))

    db.session.commit()

    return goal

@bp.delete("/<goal_id>")
@require_goal
@serialize_with(EmptyBody(), 204)
def delete_goal(goal):
    db.session.delete(goal)
    db.session.commit()

@bp.post("/<goal_id>/tasks")
@require_goal
@serialize_with(ShallowGoalWithTasks())
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

    return goal

@bp.get("/<goal_id>/tasks")
@require_goal
@serialize_with(GoalWithTasks())
def get_goal_tasks(goal):
    return goal