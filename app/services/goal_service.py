from ..models.goal import Goal
from ..models.task import Task
from ..errors.invalid_request_data_error import InvalidRequestDataError
from ..errors.record_not_found_error import RecordNotFoundError

class GoalService:
    def __init__(self, db) -> None:
        self.db = db

    def get_goals(self):
        db = self.db
        query = db.select(Goal)
        goals = db.session.scalars(query)

        return goals

    def create_goal(self, data):
        try:
            goal = Goal.from_dict(data)
        except KeyError:
            raise InvalidRequestDataError()

        db = self.db
        db.session.add(goal)
        db.session.commit()

        return goal

    def update_goal(self, goal, data):
        try:
            goal.update_from_dict(data)
        except KeyError:
            raise InvalidRequestDataError()

        db = self.db
        db.session.commit()

        return goal

    def delete_goal(self, goal):
        db = self.db
        db.session.delete(goal)
        db.session.commit()

    def set_goal_tasks(self, goal, data):
        try:
            task_ids = data["task_ids"]
            tasks = []
            for task_id in task_ids:
                task = Task.get_by_id(task_id)
                tasks.append(task)

            goal.tasks = tasks
        except (KeyError, RecordNotFoundError):
            raise InvalidRequestDataError()

        db = self.db
        db.session.commit()

        return goal
