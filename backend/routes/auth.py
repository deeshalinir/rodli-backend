from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
import bcrypt

from database.db import db
from database.models import User


auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


def _validate_role(role: str) -> bool:
    return role in {"worker", "client"}


@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json() or {}
    name = data.get("name")
    email = data.get("email")
    password = data.get("password")
    role = data.get("role")

    if not all([name, email, password, role]):
        return jsonify({"message": "All fields are required"}), 400

    if not _validate_role(role):
        return jsonify({"message": "Role must be 'worker' or 'client'"}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({"message": "Email already registered"}), 409

    hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

    user = User(name=name, email=email, password=hashed_password, role=role)
    db.session.add(user)
    db.session.commit()

    return jsonify({"message": "User registered"}), 201


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json() or {}
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"message": "Email and password are required"}), 400

    user = User.query.filter_by(email=email).first()
    if not user or not bcrypt.checkpw(password.encode("utf-8"), user.password.encode("utf-8")):
        return jsonify({"message": "Invalid credentials"}), 401

    token = create_access_token(identity=user.user_id, additional_claims={"role": user.role})

    return jsonify({"token": token, "user_id": user.user_id, "role": user.role}), 200
