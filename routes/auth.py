from flask import Blueprint, request, session
from pymongo.errors import DuplicateKeyError

from auth_utils import hash_password, verify_password
from db import db

auth_bp = Blueprint("auth", __name__, url_prefix="/api/auth")


@auth_bp.post("/register")
def register():
    data = request.get_json(silent=True) or request.form
    username = data.get("username")
    password = data.get ("password")
    confPassword = data.get("confPassword")
    if not username or not password:
        return {'error': 'username and password required'}, 400
    if not password or not confPassword:
        return {'error': 'password and confpassword both required'}, 400
    if password != confPassword:
        return {"error": "passwords did not match"}, 400
    
    try:
        db.users.insert_one({
            "username": username,
            "password_hash": hash_password(password)
        })
    except DuplicateKeyError:
        return {'error': 'username taken'}, 409

    return {"message": "registered"}, 201


@auth_bp.post("/login")
def login():
    data = request.get_json(silent=True) or request.form
    user = db.users.find_one({"username": data.get("username")})
    if user is None or not verify_password(user["password_hash"], data.get("password", "")):
        return {'error': 'invalid credentials'}, 401

    session["user_id"] = str(user["_id"])
    return {"message": "logged in"}


@auth_bp.post("/logout")
def logout():
    session.clear()
    return {"message": "Logged out"}