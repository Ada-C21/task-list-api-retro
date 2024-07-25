from app.models.session import Session
from app.errors.invalid_request_data_error import InvalidRequestDataError
from app.errors.record_not_found_error import RecordNotFoundError
from app.bcrypt import bcrypt
from app.dto.user_dto import UserDto
from sqlalchemy.exc import DataError
from datetime import datetime, timezone, timedelta

SESSION_MINUTES = 30

class SessionService:
    def __init__(self, db) -> None:
        self.db = db

    def login(self, email, password, user_service, now_provider=datetime.now):
        try:
            user = user_service.get_by_auth(email, password)
        except RecordNotFoundError:
            raise InvalidRequestDataError()

        expires_at = now_provider(timezone.utc) + timedelta(minutes=SESSION_MINUTES)
        session = Session(user_id=user.id, expires_at=expires_at)

        db = self.db
        db.session.add(session)
        db.session.commit()

        return session

    def logout(self, id, active_session_id, now_provider=datetime.now):
        if id != active_session_id:
            raise InvalidRequestDataError()

        session = Session.get_by_id(id)
        self.expire_session(session, now_provider)

    def get_active(self, id, now_provider=datetime.now):
        db = self.db
        query = db.select(Session).where(Session.id == id,
                                         Session.expires_at > now_provider(timezone.utc))
        try:
            model = db.session.scalar(query)
        except DataError:
            raise InvalidRequestDataError(Session, id)

        if not model:
            raise InvalidRequestDataError(Session, id)
        
        self.extend_session(model, now_provider)
        
        return model

    def extend_session(self, session, now_provider=datetime.now):
        db = self.db
        session.expires_at = now_provider(timezone.utc) + timedelta(minutes=SESSION_MINUTES)
        db.session.commit()

    def expire_session(self, session, now_provider=datetime.now):
        db = self.db
        session.expires_at = now_provider(timezone.utc) - timedelta(minutes=SESSION_MINUTES)
        db.session.commit()
