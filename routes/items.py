from flask import Blueprint, request

from auth_utils import Login_required
from db import db

items_bp = Blueprint("items", __name__, url_prefix="/api/items")


def serialize(doc):
    doc["_id"] = str(doc["_id"])
    return doc


@items_bp.get("/")
def list_items():
    return [serialize(p) for p in db.items.find()]


@items_bp.post("/")
@Login_required
def add_item():
    data = request.get_json(silent=True) or request.form
    if not data or "name" not in data:
        return {"error": "name is required"}, 400

    item = {
        "name": data["name"],
        "description": data.get("description", ""),
    }
    db.items.insert_one(item)
    return serialize(item), 201
