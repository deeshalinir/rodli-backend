from database.db import db


class WorkerService(db.Model):
    __tablename__ = "worker_services"

    service_id = db.Column(db.Integer, primary_key=True)
    worker_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Float, nullable=False)
    location = db.Column(db.String(120), nullable=False)

    saved_by = db.relationship("SavedService", backref="service", lazy=True, cascade="all, delete-orphan")

    def to_dict(self):
        return {
            "service_id": self.service_id,
            "worker_id": self.worker_id,
            "title": self.title,
            "description": self.description,
            "price": self.price,
            "location": self.location,
        }
