from flask import Blueprint, request
from ..db import db
from .goal_helpers import require_goal
from .helpers import serialize_with, handle_invalid_data
from ..serializers.one_goal import OneGoal
from ..serializers.list_of_goals import ListOfGoals
from ..serializers.empty_body import EmptyBody
from ..serializers.shallow_goal_with_tasks import ShallowGoalWithTasks
from ..serializers.goal_with_tasks import GoalWithTasks
from ..services.goal_service import GoalService

bp = Blueprint("goal", __name__, url_prefix="/goals")

@bp.get("")
@serialize_with(ListOfGoals())
def goal_index():
    return GoalService(db).get_goals()

@bp.get("/<goal_id>")
@require_goal
@serialize_with(OneGoal())
def get_one_goal(goal):
    return goal

@bp.post("")
@serialize_with(OneGoal(), 201)
@handle_invalid_data
def create_goal():
    return GoalService(db).create_goal(request.get_json())

@bp.put("/<goal_id>")
@require_goal
@serialize_with(OneGoal())
def update_goal(goal):
    return GoalService(db).update_goal(goal, request.get_json())

@bp.delete("/<goal_id>")
@require_goal
@serialize_with(EmptyBody(), 204)
def delete_goal(goal):
    return GoalService(db).delete_goal(goal)

@bp.post("/<goal_id>/tasks")
@require_goal
@serialize_with(ShallowGoalWithTasks())
@handle_invalid_data
@handle_invalid_data
def set_goal_tasks(goal):
    return GoalService(db).set_goal_tasks(goal, request.get_json())

@bp.get("/<goal_id>/tasks")
@require_goal
@serialize_with(GoalWithTasks())
def get_goal_tasks(goal):
    return goal