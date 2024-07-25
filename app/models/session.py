from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, types, text
from typing import Optional
from ..db import db
import datetime
from .model_mixin import ModelMixin
import uuid

class Session(db.Model, ModelMixin):
    id: Mapped[uuid.UUID] = mapped_column(types.Uuid, primary_key=True,
                                          server_default=text("gen_random_uuid()"))
    user_id: Mapped[str] = mapped_column(ForeignKey('user.id'))
    user: Mapped["User"] = relationship()
    expires_at: Mapped[datetime.datetime] = mapped_column(types.DateTime(timezone=True))

    def to_dict(self):
        user_dict = {
            "id": self.user.id,
            "name": self.user.name,
            "email": self.user.email,
        }

        return {
            "id": self.id,
            "user": user_dict,
        }
