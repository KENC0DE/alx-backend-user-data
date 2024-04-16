#!/usr/bin/env python3
"""
Basic Authentication
"""
from api.v1.auth.auth import Auth


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
