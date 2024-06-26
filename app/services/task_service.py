from app.models.task import Task
from app.errors.invalid_request_data_error import InvalidRequestDataError
import datetime
from ..ext.slack import notify_complete

class TaskService:
    def __init__(self, db) -> None:
        self.db = db

    def get_tasks(self, sort_dir=None):
        db = self.db
        if sort_dir == "asc":
            query = db.select(Task).order_by(Task.title)
        elif sort_dir == "desc":
            query = db.select(Task).order_by(Task.title.desc())
        else:
            query = db.select(Task)

        tasks = db.session.scalars(query)

        return tasks

    def create_task(self, data):
        try:
            task = Task.from_dict(data)
        except KeyError:
            raise InvalidRequestDataError()

        db = self.db
        db.session.add(task)
        db.session.commit()

        return task

    def update_task(self, task, data):
        try:
            task.update_from_dict(data)
        except KeyError:
            raise InvalidRequestDataError()

        db = self.db
        db.session.commit()

        return task

    def delete_task(self, task):
        db = self.db
        db.session.delete(task)
        db.session.commit()

    def mark_complete(self, task):
        task.completed_at = datetime.datetime.now(datetime.timezone.utc)

        db = self.db
        db.session.commit()

        notify_complete(task)

        return task

    def mark_incomplete(self, task):
        task.completed_at = None

        db = self.db
        db.session.commit()

        return task
