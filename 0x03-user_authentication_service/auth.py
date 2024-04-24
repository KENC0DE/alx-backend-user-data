#!/usr/bin/env python3
"""Auth Module
"""
from sqlalchemy.orm.exc import NoResultFound
from user import User
from db import DB
import bcrypt
import uuid


def _hash_password(password: str) -> str:
    """Returns hashed bytes of a given password"""
    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    return hashed


def _generate_uuid() -> str:
    """ Generates UUID and return string representation of it"""
    return str(uuid.uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """ Registers a user in the database
        Returns: User Object
        """

        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            hashed_password = _hash_password(password)
            user = self._db.add_user(email, hashed_password)

            return user

        else:
            raise ValueError(f'User {email} already exists')

    def valid_login(self, email: str, password: str) -> bool:
        """check if the login is valid or not"""
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return False

        p1 = password.encode('utf-8')
        p2 = user.hashed_password

        return bcrypt.checkpw(p1, p2)

    def create_session(self, email: str) -> str:
        """Retuns sessoin ID"""
        try:
            user = self._db.find_user_by(email=email)
            s_id = _generate_uuid()
            user.session_id = s_id
            self._db._session.commit()
            return s_id
        except Exception:
            return None

    def get_user_from_session_id(self, session_id: str) -> User:
        """Return user instance bassed on session id"""
        if not session_id:
            return None

        try:
            user = self._db.find_user_by(session_id=session_id)
            return user
        except NoResultFound:
            return None

    def destroy_session(self, user_id: int) -> None:
        """ Destory user's session ID"""
        try:
            user = self._db.find_user_by(id=user_id)
            self._db.update_user(user.id, session_id=None)
        except Exception:
            return None

    def get_reset_password_token(self, email: str) -> str:
        """Return token to reset password"""
        try:
            user = self._db.find_user_by(email=email)
            token = _generate_uuid()
            user.reset_token = token
            return token
        except NoResultFound:
            raise ValueError
