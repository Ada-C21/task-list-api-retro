from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..db import db
from .model_mixin import ModelMixin

class Goal(db.Model, ModelMixin):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str]
    tasks: Mapped[list["Task"]] = relationship(back_populates="goal")

    def update_from_dict(self, data):
        self.title = data["title"]

    def to_dict(self):
        return dict(
            id=self.id,
            title=self.title,
        )
    
    @classmethod
    def from_dict(cls, data):
        return Goal(
            title=data["title"],
        )
