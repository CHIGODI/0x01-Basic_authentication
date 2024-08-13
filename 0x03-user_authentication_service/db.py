#!/usr/bin/env python3

"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from user import Base, User
from typing import Mapping
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError
import bcrypt


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db")
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
        """Add user to db"""
        if email and hashed_password:
            user: User = User(email=email, hashed_password=hashed_password)
            self._session.add(user)
            self._session.commit()
            return user

    def find_user_by(self, **kwargs) -> User:
        """Find user in db"""
        try:
            user: User = self._session.query(User).filter_by(**kwargs).one()
        except NoResultFound:
            raise NoResultFound
        except InvalidRequestError:
            raise InvalidRequestError
        return user

    def update_user(self, user_id: int, **kwargs) -> None:
        """Update user object"""
        user = self.find_user_by(id=user_id)
        if user:
            for key, val in kwargs.items():
                if not hasattr(user, key):
                    raise ValueError
                setattr(user, key, val),
            self._session.commit()
