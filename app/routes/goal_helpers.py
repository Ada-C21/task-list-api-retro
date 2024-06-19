from functools import wraps
from .helpers import validate_model
from ..models.goal import Goal

# more robust decorator (uses wraps and variadic params)
def require_goal(fn):
    @wraps(fn)
    def wrapper(*args, goal_id, **kwargs):
        goal = validate_model(Goal, goal_id)
        return fn(*args, goal=goal, **kwargs)

    return wrapper

