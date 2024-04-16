#!/usr/bin/env python3
"""
Basic Authentication
"""
from api.v1.auth.auth import Auth
import base64


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
