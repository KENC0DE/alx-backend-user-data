#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm.session import Session
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from typing import TypeVar
from typing import Dict
from user import User
from user import Base


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """ Adds user to database
        Return: User Object
        """
        user = User(email=email, hashed_password=hashed_password)
        self._session.add(user)
        self._session.commit()

        return user

    def find_user_by(self, **kwargs) -> User:
        """Returns first rrow found in users table
        as filtered by methods input arguments
        """
        user_keys = User.__table__.columns.keys()
        for key in kwargs.keys():
            if key not in user_keys:
                raise InvalidRequestError
        result = self._session.query(User).filter_by(**kwargs).first()
        if result is None:
            raise NoResultFound
        return result

    def update_user(self, user_id: int, **kwargs) -> None:
        """Locate and upadate user"""
        user = self.find_user_by(id=user_id)
        if user:
            keys = User.__table__.columns.keys()
            for key, val in kwargs.items():
                if key not in keys:
                    raise ValueError
                setattr(user, key, val)

            self._session.commit()
