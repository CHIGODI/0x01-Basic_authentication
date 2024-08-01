#!/usr/bin/env python3
"""Encryption"""

import bcrypt


def hash_password(password: str) -> bytes:
    """Hash password"""
    return bcrypt.hashpw(password.encode('utf-8'),  bcrypt.gensalt())


def is_valid(hashed_password: bytes, password: str) -> bool:
    """Check if password macthes hashed password"""
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)
