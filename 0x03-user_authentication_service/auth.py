#!/usr/bin/env python3
"""Auth module"""

import bcrypt
from db import DB
from user import User


def _hash_password(password: str) -> bytes:
    """Hash a password for storing."""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


class Auth:
    """Auth class to interact with the authentication database.
    """
    def __init__(self):
        self._db = DB()

    def auth_register(self, email: str, password: str) -> User:
        """"""
        user = DB.find_user_by(email=email)
        if user:
            raise ValueError(f"User {email} already exists")
        new_user = DB.add_user(email=email,
                               password=_hash_password(password))
        return new_user
