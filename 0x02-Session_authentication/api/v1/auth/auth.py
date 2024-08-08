#!/usr/bin/env python3
""" Auth class"""

from flask import request
from typing import List, TypeVar
import os


class Auth:
    """Auth class"""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Determines if the path requires authentication."""
        if path is None or excluded_paths is None or len(excluded_paths) == 0:
            return True

        if path[-1] != '/':
            path += '/'

        for excluded_path in excluded_paths:
            if excluded_path.endswith('*'):
                if path.startswith(excluded_path[:-1]):
                    return False
                else:
                    return True
            elif excluded_path == path:
                return False
            else:
                return True

    def authorization_header(self, request=None) -> str:
        """authorization_header"""
        authorization = request.headers.get('Authorization')
        if request is None or authorization is None:
            return None
        return authorization

    def current_user(self, request=None) -> TypeVar('User'):  # type: ignore
        """current_user return none"""
        return None

    def session_cookie(self, request=None):
        """return a cookie val from request"""
        if request:
            session_name = f'{os.getenv("SESSION_NAME")}='
            result = request.headers.get('Cookie')
            return result[len(session_name):]
        return None
