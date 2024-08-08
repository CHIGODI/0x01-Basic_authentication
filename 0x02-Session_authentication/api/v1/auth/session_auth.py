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
            session_id = str(uuid.uuid4())
            SessionAuth.user_id_by_session_id[session_id] = user_id
            return session_id
        return None

    def user_id_for_session_id(self,
                               session_id: str = None) -> str:
        """Return user based on session ID"""
        if session_id and isinstance(session_id, str):
            return SessionAuth.user_id_by_session_id.get(session_id)
        return None
