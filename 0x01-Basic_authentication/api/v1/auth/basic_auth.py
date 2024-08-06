#!/usr/bin/env python3
"""Basic Auth"""
from api.v1.auth.auth import Auth


class BasicAuth(Auth):
    """Basic Auth"""
    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """extract base64 from header"""
        if authorization_header is None:
            return None
        elif type(authorization_header) is not str:
            return None
        elif authorization_header[0:4] + '' != 'Basic ':
            return None

        return authorization_header[4:-1]
