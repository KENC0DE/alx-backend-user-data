#!/usr/bin/env python3
"""
Basic Authentication
"""
from api.v1.auth.auth import Auth
from flask import request
import base64
from models.user import User
from typing import TypeVar


class BasicAuth(Auth):
    """basic authentiaction class
    """
    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """extract base64 authorizaton header"""
        ath = authorization_header
        if ath and type(ath) is str and ath.startswith('Basic '):
            return ath[6:]

        return None

    def decode_base64_authorization_header(self,
                                           base64_authorization_header: str
                                           ) -> str:
        """Decode base64 authorization header"""
        a64 = base64_authorization_header
        if a64 and type(a64) is str:
            try:
                code64 = base64.b64decode(a64)
                return code64.decode('utf-8')
            except Exception:
                return None

        return None

    def extract_user_credentials(self,
                                 decoded_base64_authorization_header: str
                                 ) -> (str, str):
        """ extract user credtials"""
        d64 = decoded_base64_authorization_header
        if d64 and type(d64) is str and ':' in d64:
            return tuple(d64.split(':', 1))

        return (None, None)

    def user_object_from_credentials(self, user_email: str,
                                     user_pwd: str) -> TypeVar('User'):
        """user object from credentials"""
        ue = user_email
        up = user_pwd
        if ue and up and type(ue) is str and type(up) is str:
            try:
                userl = User.search({'email': user_email})
                if userl and userl != []:
                    for user in userl:
                        if user.is_valid_password(user_pwd):
                            return user
            except Exception:
                return None

        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """ overloads Auth and retrieves the User instance for a request """
        auth_header = self.authorization_header(request)
        if not auth_header:
            return None

        encoded = self.extract_base64_authorization_header(auth_header)
        if not encoded:
            return None

        decoded = self.decode_base64_authorization_header(encoded)
        if not decoded:
            return None

        email, pwd = self.extract_user_credentials(decoded)
        if not email or not pwd:
            return None

        user = self.user_object_from_credentials(email, pwd)
        return user
