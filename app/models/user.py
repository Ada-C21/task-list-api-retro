from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from typing import Optional
from ..db import db
import datetime
from .model_mixin import ModelMixin

class User(db.Model, ModelMixin):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str]
    email: Mapped[str] = mapped_column(unique=True)
    pwd_hash: Mapped[str]

    def to_dict(self):
        pass
    
    @classmethod
    def from_dict(cls, data):
        pass