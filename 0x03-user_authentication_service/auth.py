#!/usr/bin/env python3
"""Auth Module
"""
import bcrypt


def _hash_password(pwd: str) -> str:
    """Returns hashed bytes of a given password"""
    hashed_pwd = bcrypt.hashpw(pwd.encode(), bcrypt.gensalt())
    return hashed_pwd
