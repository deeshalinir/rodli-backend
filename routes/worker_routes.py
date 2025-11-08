from flask import Blueprint, request, jsonify
from database.db import db
from database.models.worker import Worker

worker_bp = Blueprint("worker", __name__)

# --------------------------------------------------------------------
# 1️⃣  Get all workers (optionally filter by region or category)
# --------------------------------------------------------------------
@worker_bp.get("/")
def get_workers():
    region = request.args.get("region")
    category = request.args.get("category")

    query = Worker.query
    if region:
        query = query.filter(Worker.region.ilike(f"%{region}%"))
    if category:
        query = query.filter(Worker.category.ilike(f"%{category}%"))

    workers = query.all()
    return jsonify([w.to_dict() for w in workers])


# --------------------------------------------------------------------
# 2️⃣  Get a single worker by ID
# --------------------------------------------------------------------
@worker_bp.get("/<int:worker_id>")
def get_worker(worker_id):
    worker = Worker.query.get(worker_id)
    if not worker:
        return jsonify({"error": "Worker not found"}), 404
    return jsonify(worker.to_dict())


# --------------------------------------------------------------------
# 3️⃣  Add a new worker
# --------------------------------------------------------------------
@worker_bp.post("/")
def add_worker():
    data = request.get_json()
    try:
        worker = Worker(
            name=data["name"],
            category=data.get("category"),
            region=data.get("region"),
            phone=data.get("phone"),
            bio=data.get("bio"),
            rating=data.get("rating", 0),
        )
        db.session.add(worker)
        db.session.commit()
        return jsonify(worker.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400


# --------------------------------------------------------------------
# 4️⃣  Update worker info
# --------------------------------------------------------------------
@worker_bp.put("/<int:worker_id>")
def update_worker(worker_id):
    worker = Worker.query.get(worker_id)
    if not worker:
        return jsonify({"error": "Worker not found"}), 404

    data = request.get_json()
    for key, value in data.items():
        if hasattr(worker, key):
            setattr(worker, key, value)

    db.session.commit()
    return jsonify(worker.to_dict())


# --------------------------------------------------------------------
# 5️⃣  Delete worker
# --------------------------------------------------------------------
@worker_bp.delete("/<int:worker_id>")
def delete_worker(worker_id):
    worker = Worker.query.get(worker_id)
    if not worker:
        return jsonify({"error": "Worker not found"}), 404

    db.session.delete(worker)
    db.session.commit()
    return jsonify({"message": "Worker deleted successfully"})
