from sqlalchemy.orm import Mapped, mapped_column, relationship
from app import db


class Goal(db.Model):
    goal_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str]
    tasks: Mapped[list["Task"]] = relationship(back_populates="goal")

    def to_dict(self):
        return dict(
            id=self.goal_id,
            title=self.title,
        )
    
    @classmethod
    def from_dict(cls, data):
        return Goal(
            title=data["title"],
        )