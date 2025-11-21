from datetime import datetime
from database.db import db


class User(db.Model):
    __tablename__ = "users"

    user_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    services = db.relationship("WorkerService", backref="worker", lazy=True, cascade="all, delete-orphan")
    saved_services = db.relationship("SavedService", backref="client", lazy=True, cascade="all, delete-orphan")
    contact_requests = db.relationship("ContactRequest", backref="worker", lazy=True, cascade="all, delete-orphan")
