#!/usr/bin/env python3
"""SessionExpAuth class"""
from api.v1.auth.session_auth import SessionAuth
import os
import datetime
from datetime import timedelta


class SessionExpAuth(SessionAuth):
    """"""
    def __init__(self) -> None:
        """Initiliaize attributes"""
        super().__init__()
        self.session_duration = int(os.getenv('SESSION_DURATION'), 0)

    def create_session(self, user_id=None):
        """Create a session with expiration"""
        session_id = super().create_session(user_id)
        if not session_id:
            return None
        created_at = datetime.now()
        session_dictionary = {'user_id': user_id,
                              'created_at': created_at
                              }
        self.user_id_by_session_id[session_id] = session_dictionary
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """Retrieve user ID based on session ID, considering expiration"""
        if not session_id:
            return None

        session_data = self.user_id_by_session_id.get(session_id)
        if not session_data:
            return None

        user_id = session_data.get('user_id')
        created_at = session_data.get('created_at')

        if self.session_duration <= 0:
            return user_id

        if not created_at:
            return None

        # Check if the session is expired
        if datetime.now() > created_at + timedelta(
                seconds=self.session_duration):
            return None

        return user_id
