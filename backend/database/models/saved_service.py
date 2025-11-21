from database.db import db


class SavedService(db.Model):
    __tablename__ = "saved_services"

    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False)
    service_id = db.Column(db.Integer, db.ForeignKey("worker_services.service_id"), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "client_id": self.client_id,
            "service_id": self.service_id,
        }
