from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity

from database.db import db
from database.models import User, WorkerService, SavedService


client_bp = Blueprint("client", __name__, url_prefix="/client")


def _ensure_client_role():
    claims = get_jwt()
    return claims.get("role") == "client"


@client_bp.route("/services", methods=["GET"])
def list_all_services():
    services = WorkerService.query.all()
    return jsonify([service.to_dict() for service in services]), 200


@client_bp.route("/save", methods=["POST"])
@jwt_required()
def save_service():
    if not _ensure_client_role():
        return jsonify({"message": "Client role required"}), 403

    user_id = get_jwt_identity()
    data = request.get_json() or {}
    service_id = data.get("service_id")

    if not service_id:
        return jsonify({"message": "Service ID is required"}), 400

    service = WorkerService.query.get(service_id)
    if not service:
        return jsonify({"message": "Service not found"}), 404

    existing = SavedService.query.filter_by(client_id=user_id, service_id=service_id).first()
    if existing:
        return jsonify({"message": "Service already saved"}), 200

    saved = SavedService(client_id=user_id, service_id=service_id)
    db.session.add(saved)
    db.session.commit()

    return jsonify({"message": "Service saved", "saved": saved.to_dict()}), 201


@client_bp.route("/save", methods=["GET"])
@jwt_required()
def list_saved_services():
    if not _ensure_client_role():
        return jsonify({"message": "Client role required"}), 403

    user_id = get_jwt_identity()
    saved = SavedService.query.filter_by(client_id=user_id).all()

    response = []
    for item in saved:
        service = WorkerService.query.get(item.service_id)
        service_data = service.to_dict() if service else None
        response.append({"id": item.id, "service": service_data})

    return jsonify(response), 200
