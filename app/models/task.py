from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from typing import Optional
from app import db
import datetime

class Task(db.Model):
    task_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str]
    description: Mapped[str]
    completed_at: Mapped[Optional[datetime.datetime]]
    goal_id: Mapped[Optional[int]] = mapped_column(ForeignKey("goal.goal_id"))
    goal: Mapped[Optional["Goal"]] = relationship(back_populates="tasks")

    def is_complete(self):
        return self.completed_at is not None

    def to_dict(self):
        data = dict(
            id=self.task_id,
            title=self.title,
            description=self.description,
            is_complete=self.is_complete(),
        )

        if self.goal_id:
            data["goal_id"] = self.goal_id

        return data
    
    @classmethod
    def from_dict(cls, data):
        return Task(
            title=data["title"],
            description=data["description"],
        )