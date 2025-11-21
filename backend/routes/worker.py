from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity

from database.db import db
from database.models import User, WorkerService, ContactRequest


worker_bp = Blueprint("worker", __name__, url_prefix="/worker")


def _ensure_worker_role():
    claims = get_jwt()
    return claims.get("role") == "worker"


@worker_bp.route("/services", methods=["POST"])
@jwt_required()
def create_service():
    if not _ensure_worker_role():
        return jsonify({"message": "Worker role required"}), 403

    user_id = get_jwt_identity()
    data = request.get_json() or {}
    title = data.get("title")
    description = data.get("description")
    price = data.get("price")
    location = data.get("location")

    if not all([title, price, location]):
        return jsonify({"message": "Title, price, and location are required"}), 400

    try:
        price_value = float(price)
    except (TypeError, ValueError):
        return jsonify({"message": "Price must be a number"}), 400

    service = WorkerService(
        worker_id=user_id,
        title=title,
        description=description,
        price=price_value,
        location=location,
    )
    db.session.add(service)
    db.session.commit()

    return jsonify({"message": "Service created", "service": service.to_dict()}), 201


@worker_bp.route("/services", methods=["GET"])
@jwt_required()
def list_services():
    if not _ensure_worker_role():
        return jsonify({"message": "Worker role required"}), 403

    user_id = get_jwt_identity()
    services = WorkerService.query.filter_by(worker_id=user_id).all()
    return jsonify([service.to_dict() for service in services]), 200


@worker_bp.route("/requests", methods=["GET"])
@jwt_required()
def list_requests():
    if not _ensure_worker_role():
        return jsonify({"message": "Worker role required"}), 403

    user_id = get_jwt_identity()
    requests = ContactRequest.query.filter_by(worker_id=user_id).all()
    return jsonify([req.to_dict() for req in requests]), 200
