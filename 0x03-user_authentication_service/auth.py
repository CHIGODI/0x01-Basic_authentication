#!/usr/bin/env python3
"""Auth module"""

import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound


def _hash_password(password: str) -> bytes:
    """Hash a password for storing."""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


class Auth:
    """Auth class to interact with the authentication database.
    """
    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Register a new user with an email and password."""
        if isinstance(email, str) and isinstance(password, str):
            try:
                self._db.find_user_by(email=email)
            except NoResultFound:
                hashed_password = _hash_password(password)
                new_user = self._db.add_user(email=email,
                                             hashed_password=hashed_password)
                return new_user
            else:
                raise ValueError(f"User {email} already exists")

    def valid_login(self, email: str, password: str) -> bool:
        """Checks if user login are valid"""
        try:
            user = self._db.find_user_by(email=email)
        except Exception as e:
            return False

        if bcrypt.checkpw(password.encode('utf-8'), user.hashed_password):
            return True
        return False
