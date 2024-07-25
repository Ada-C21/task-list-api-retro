from app.models.user import User
from app.errors.invalid_request_data_error import InvalidRequestDataError
from app.errors.record_not_found_error import RecordNotFoundError
from app.bcrypt import bcrypt
from app.dto.user_dto import UserDto
from sqlalchemy.exc import IntegrityError

class UserService:
    def __init__(self, db) -> None:
        self.db = db

    def create_user(self, name, email, password):
        pwd_hash = bcrypt.generate_password_hash(password).decode("utf-8")
        user = User(name=name, email=email, pwd_hash=pwd_hash)

        db = self.db
        db.session.add(user)
        try:
            db.session.commit()
        except IntegrityError:
            raise InvalidRequestDataError()

        return UserDto(user)

    def get_by_auth(self, email, password):
        user = User.get_by_email(email)
        matches = bcrypt.check_password_hash(user.pwd_hash, password)

        if not matches:
            raise RecordNotFoundError()
        
        return UserDto(user)
