from ..db import db
from flask import abort, make_response
from functools import wraps

def validate_model(cls, model_id):
    query = db.select(cls).where(cls.id == model_id)
    model = db.session.scalar(query)

    if not model:
        abort(make_response(dict(
            details=f"Unknown {cls.__name__} id: {model_id}"
        ), 404))

    return model

def serialize_with(serializer, status=200):
    def decorator(fn):
        @wraps(fn)
        def inner(*args, **kwargs):
            result = fn(*args, **kwargs)
            return serializer.serialize(result), status

        return inner
    
    return decorator
