from .helpers import validate_model
from functools import wraps
from ..models.task import Task

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
