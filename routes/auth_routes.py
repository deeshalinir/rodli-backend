from flask import Blueprint, request, jsonify, current_app
from werkzeug.security import generate_password_hash, check_password_hash
from database.db import db
from database.models.user import User
import jwt, datetime

auth_bp = Blueprint("auth", __name__)

@auth_bp.post("/register")
def register():
    data = request.get_json()
    email = data["email"].lower().strip()
    if User.query.filter_by(email=email).first():
        return jsonify({"error": "Email already registered"}), 409

    user = User(
        email=email,
        full_name=data.get("full_name"),
        password_hash=generate_password_hash(data["password"])
    )
    db.session.add(user)
    db.session.commit()
    return jsonify({"id": user.id, "email": user.email})

@auth_bp.post("/login")
def login():
    data = request.get_json()
    user = User.query.filter_by(email=data["email"].lower().strip()).first()
    if not user or not check_password_hash(user.password_hash, data["password"]):
        return jsonify({"error": "Invalid credentials"}), 401

    token = jwt.encode(
        {"sub": user.id, "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=12)},
        current_app.config["JWT_SECRET"], algorithm="HS256"
    )
    return jsonify({"access_token": token, "user": {"id": user.id, "email": user.email, "role": user.role}})
