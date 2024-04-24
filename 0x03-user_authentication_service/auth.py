#!/usr/bin/env python3
"""Auth Module
"""
from sqlalchemy.orm.exc import NoResultFound
from user import User
from db import DB
import bcrypt


def _hash_password(password: str) -> str:
    """Returns hashed bytes of a given password"""
    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    return hashed


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
