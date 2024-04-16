#!/usr/bin/env python3
"""
The Auth Class Module
"""
from flask import request
from typing import List, TypeVar


class Auth:
    """Authentication class
    """
    def require_auth(self, path: str, exluded_path: List[str]) -> bool:
        """ Return False for now"""
        return False

    def authorization_header(self, request=None) -> str:
        """Returns flask request"""
        return request

    def current_user(self, request=None) -> TypeVar('User'):
        """Returns flask request"""
        return request
