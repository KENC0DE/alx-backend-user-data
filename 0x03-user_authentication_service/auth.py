#!/usr/bin/env python3
"""Auth Module
"""
import bcrypt


def _hash_password(password: str) -> str:
    """Returns hashed bytes of a given password"""
    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    return hashed
