#!/usr/bin/env python3
"""Basic Auth"""
from api.v1.auth.auth import Auth
import base64
from models.user import User
from typing import TypeVar


class BasicAuth(Auth):
    """Basic Auth"""
    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """extract authorization header"""
        if authorization_header is None:
            return None
        if not isinstance(authorization_header, str):
            return None
        if not authorization_header.startswith('Basic '):
            return None
        return authorization_header[len('Basic '):]

    def decode_base64_authorization_header(self,
                                           base64_authorization_header: str)\
            -> str:
        """decode base 64"""
        if base64_authorization_header is None:
            return None
        if not isinstance(base64_authorization_header, str):
            return None
        try:
            decoded_bytes = base64.b64decode(base64_authorization_header)
            return decoded_bytes.decode('utf-8')
        except Exception:
            return None

    def extract_user_credentials(self,
                                 decoded_base64_authorization_header: str)\
            -> (str, str):  # type: ignore
        """exctracts user credentials"""
        if decoded_base64_authorization_header is None:
            return None, None
        if not isinstance(decoded_base64_authorization_header, str):
            return None, None
        if ':' not in decoded_base64_authorization_header:
            return None, None

        values = decoded_base64_authorization_header.split(':')
        pwd = values[1:]
        return values[0], (':').join(pwd)

    def user_object_from_credentials(self, user_email: str,
                                     user_pwd: str)\
            -> TypeVar('User'):  # type: ignore
        """return user instance based on email and passsword"""
        if not isinstance(user_email, str) or not isinstance(user_pwd, str):
            return None

        # fetch possible user object with email = email
        users = User.search({'email': user_email})

        if len(users) == 0:
            return None

        for user in users:
            if user.is_valid_password(user_pwd):
                return user
        return None

    def current_user(self, request=None) -> TypeVar('User'):  # type: ignore
        """Retrieve the User instance for a request"""
        auth_header = self.authorization_header(request)
        if not auth_header:
            return None

        base64_auth = self.extract_base64_authorization_header(auth_header)
        if not base64_auth:
            return None

        decoded_auth = self.decode_base64_authorization_header(base64_auth)
        if not decoded_auth:
            return None

        user_email, user_pwd = self.extract_user_credentials(decoded_auth)
        if not user_email or not user_pwd:
            return None

        return self.user_object_from_credentials(user_email, user_pwd)
