#!/usr/bin/env python3
"""
Session Authentication
"""
from api.v1.auth.auth import Auth
from uuid import uuid4
from models.user import User


class SessionAuth(Auth):
    """Session class inherits from Auth"""
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """Create session"""
        if not user_id or type(user_id) is not str:
            return None

        session_id = str(uuid4())
        self.user_id_by_session_id.update({session_id: user_id})
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """ Returns a User Id based on Session Id"""
        if not session_id or type(session_id) is not str:
            return None

        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None) -> object:
        """return User instance"""
        u_id = self.user_id_for_session_id(
            self.session_cookie(request)
        )
        return User.get(u_id)

    def destroy_session(self, request=None):
        """Deletes de user session / logout"""

        if request is None:
            return False

        session_id = self.session_cookie(request)
        if session_id is None:
            return False

        user_id = self.user_id_for_session_id(session_id)

        if not user_id:
            return False

        try:
            del self.user_id_by_session_id[session_id]
        except Exception:
            pass

        return True
