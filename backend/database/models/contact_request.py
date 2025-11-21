from datetime import datetime
from database.db import db


class ContactRequest(db.Model):
    __tablename__ = "contact_requests"

    id = db.Column(db.Integer, primary_key=True)
    worker_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False)
    client_name = db.Column(db.String(120), nullable=False)
    message = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "worker_id": self.worker_id,
            "client_name": self.client_name,
            "message": self.message,
            "date": self.date.isoformat() if self.date else None,
        }
