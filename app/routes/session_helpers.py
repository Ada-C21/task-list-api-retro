from flask import request, abort, make_response, g
from functools import wraps
from ..services.session_service import SessionService
from ..errors.invalid_request_data_error import InvalidRequestDataError
from ..dto.user_dto import UserDto

def invalid_auth():
    abort(make_response(dict(details="Invalid authorization"), 401))

def require_auth(db):
    def decorator(fn):
        @wraps(fn)
        def wrapped(*args, **kwargs):
            # session_id = request.headers.get("SessionID", default="")
            session_id = request.cookies.get("SessionID", default="")

            session_service = SessionService(db)

            try:
                session = session_service.get_active(session_id)
            except InvalidRequestDataError:
                invalid_auth()

            user = UserDto(session.user)
            g.user = user
            g.session_id = session_id
            result = fn(*args, **kwargs)
            response = make_response(result)
            return response
        
        return wrapped
    
    return decorator
