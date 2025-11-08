from flask import Blueprint, jsonify
from database.db import db

health_bp = Blueprint("health", __name__)

@health_bp.get("/health")
def health():
    try:
        db.session.execute(db.text("SELECT 1"))
        return jsonify({"ok": True})
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500
