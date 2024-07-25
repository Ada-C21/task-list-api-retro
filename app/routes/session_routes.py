from flask import Blueprint, request, g
from ..db import db
from .helpers import serialize_with, handle_invalid_data
from .session_helpers import require_auth
from ..serializers.one_session import OneSession
from ..serializers.empty_body import EmptyBody
from ..services.user_service import UserService
from ..services.session_service import SessionService
from ..errors.invalid_request_data_error import InvalidRequestDataError

bp = Blueprint("session", __name__, url_prefix="/sessions")

@bp.post("")
@serialize_with(OneSession(), 201)
@handle_invalid_data
def create_session():
    user_service = UserService(db)
    try:
        return SessionService(db).login(**request.get_json(), user_service=user_service)
    except TypeError:
        raise InvalidRequestDataError()

@bp.delete("/<session_id>")
@require_auth(db)
@serialize_with(EmptyBody(), 204)
@handle_invalid_data
def delete_session(session_id):
    return SessionService(db).logout(session_id, active_session_id=g.session_id)

