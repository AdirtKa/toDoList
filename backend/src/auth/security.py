"""Utility functions for password hashing and verification."""

import hashlib


def hash_password(password: str) -> str:
    """Generate a SHA-256 hash for the given password.

    Args:
        password (str): The plain-text password to hash.

    Returns:
        str: The hexadecimal SHA-256 hash of the password.
    """
    return hashlib.sha256(password.encode()).hexdigest()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify that a plain-text password matches its stored hash.

    Args:
        plain_password (str): The plain-text password provided by the user.
        hashed_password (str): The previously stored hashed password.

    Returns:
        bool: True if the password is valid, False otherwise.
    """
    return hash_password(plain_password) == hashed_password
