from flask import abort, make_response
from functools import wraps
from app.errors.invalid_request_data_error import InvalidRequestDataError
from app.errors.record_not_found_error import RecordNotFoundError

def validate_model(cls, model_id, user=None):
    try:
        model = cls.get_by_id(model_id)

        if user and model.user_id != user.id:
            raise RecordNotFoundError()

    except RecordNotFoundError:
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
def serialize_with(serializer, status=200, response_modifier=None):
    def decorator(fn):
        @wraps(fn)
        def inner(*args, **kwargs):
            result = fn(*args, **kwargs)
            serialized_result = serializer.serialize(result)
            response = make_response(serialized_result, status)

            if response_modifier:
                response_modifier(response=response, result=result)

            return response

        return inner
    
    return decorator

def handle_invalid_data(fn):
    @wraps(fn)
    def inner(*args, **kwargs):
        try:
            return fn(*args, **kwargs)
        except InvalidRequestDataError:
            abort(make_response(dict(details="Invalid data"), 400))

    return inner