from database.db import db

class Worker(db.Model):
    __tablename__ = "workers"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    category = db.Column(db.String(80), nullable=False)  # e.g. "Electrician", "Plumber"
    region = db.Column(db.String(120))                   # e.g. "Flacq", "Port Louis"
    phone = db.Column(db.String(20))
    bio = db.Column(db.Text)
    rating = db.Column(db.Float, default=0.0)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "category": self.category,
            "region": self.region,
            "phone": self.phone,
            "bio": self.bio,
            "rating": self.rating,
        }
