from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from typing import Optional
from ..db import db
import datetime
from .model_mixin import ModelMixin
from ..errors.record_not_found_error import RecordNotFoundError

class User(db.Model, ModelMixin):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str]
    email: Mapped[str] = mapped_column(unique=True)
    pwd_hash: Mapped[str]
    tasks: Mapped[list["Task"]] = relationship(back_populates="user")

    @classmethod
    def get_by_email(cls, email):
        query = db.select(cls).where(cls.email == email)
        model = db.session.scalar(query)

        if not model:
            raise RecordNotFoundError()
        
        return model
