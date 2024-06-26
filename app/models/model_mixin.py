from ..db import db
from ..errors.record_not_found_error import RecordNotFoundError

class ModelMixin:
    @classmethod
    def get_by_id(cls, model_id):
        query = db.select(cls).where(cls.id == model_id)
        model = db.session.scalar(query)

        if not model:
            raise RecordNotFoundError()
        
        return model
