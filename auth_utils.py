from functools import wraps

from argon2 import PasswordHasher
from argon2.exceptions import InvalidHashError, VerifyMismatchError
from flask import session

ph = PasswordHasher()  # Argon2ID


def hash_password(password):
    return ph.hash(password)


def verify_password(stored_hash, password):
    try:
        return ph.verify(stored_hash, password)
    except (VerifyMismatchError, InvalidHashError):
        return False


def Login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if "user_id" not in session:
            return {"error": "not logged in"}, 401
        return f(*args, **kwargs)

    return wrapper
