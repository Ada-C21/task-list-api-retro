from flask import Blueprint, request
from ..db import db
from .helpers import serialize_with, handle_invalid_data
from ..serializers.one_user import OneUser
from ..services.user_service import UserService
from ..errors.invalid_request_data_error import InvalidRequestDataError

bp = Blueprint("user", __name__, url_prefix="/users")

@bp.post("")
@serialize_with(OneUser(), 201)
@handle_invalid_data
def create_user():
    try:
        return UserService(db).create_user(**request.get_json())
    except TypeError:
        raise InvalidRequestDataError()

