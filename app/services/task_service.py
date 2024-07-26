from app.models.task import Task
from app.errors.invalid_request_data_error import InvalidRequestDataError
from app.errors.record_not_found_error import RecordNotFoundError
import datetime
from ..ext.slack import notify_complete
from sqlalchemy.exc import InvalidRequestError
from app.util import time

class TaskService:
    def __init__(self, db) -> None:
        self.db = db

    def get_tasks(self, user, sort_dir=None):
        db = self.db

        query = db.select(Task).where(Task.user_id == user.id)

        if sort_dir == "asc":
            query = query.order_by(Task.title)
        elif sort_dir == "desc":
            query = query.order_by(Task.title.desc())
        else:
            query = query.order_by(Task.id)

        tasks = db.session.scalars(query)

        return tasks

    def create_task(self, data, user):
        try:
            task = Task.from_dict(data)
            task.user_id = user.id
        except KeyError:
            raise InvalidRequestDataError()

        db = self.db
        db.session.add(task)
        db.session.commit()

        return task

    def update_task(self, task, data, user):
        if task.user_id != user.id:
            raise RecordNotFoundError()

        try:
            task.update_from_dict(data)
        except KeyError:
            raise InvalidRequestDataError()

        db = self.db
        db.session.commit()

        return task

    def delete_task(self, task, user):
        if task.user_id != user.id:
            raise RecordNotFoundError()

        db = self.db

        try:
            db.session.delete(task)
        except InvalidRequestError:
            raise RecordNotFoundError()
        
        db.session.commit()

    def mark_complete(self, task, user):
        if task.user_id != user.id:
            raise RecordNotFoundError()

        task.completed_at = time.now(datetime.timezone.utc)

        db = self.db
        db.session.commit()

        notify_complete(task)

        return task

    def mark_incomplete(self, task, user):
        if task.user_id != user.id:
            raise RecordNotFoundError()

        task.completed_at = None

        db = self.db
        db.session.commit()

        return task
