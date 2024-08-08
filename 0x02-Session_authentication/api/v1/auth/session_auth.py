#!/usr/bin/env python3
"""Session class"""

from api.v1.auth.auth import Auth
import uuid


class SessionAuth(Auth):
    """SessionAuth class"""
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """Creates session ID"""
        if user_id and isinstance(user_id, str):
            sessionID = str(uuid.uuid4())
            SessionAuth.user_id_by_session_id[sessionID] = user_id
            return sessionID
        return None
