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

# apply to route handler as
# @serialize_with(SomeSerializer(), status)
# SomeSerializer is a class that has a serialize method
# serialize takes a single argument, the data to serialize
# and returns a suitable Flask Response or something that can
# be converted to a Flask response (e.g. a dict)
def serialize_with(serializer, status=200):
    def decorator(fn):
        @wraps(fn)
        def inner(*args, **kwargs):
            result = fn(*args, **kwargs)
            return serializer.serialize(result), status

        return inner
    
    return decorator
