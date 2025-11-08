from flask import Flask
from flask_cors import CORS
from database.db import db
from routes.auth_routes import auth_bp
from routes.worker_routes import worker_bp
from routes.health_routes import health_bp
from config.settings import DATABASE_URL, JWT_SECRET
from routes.protected_routes import protected_bp

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["JWT_SECRET"] = JWT_SECRET

db.init_app(app)
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})

# Register blueprints
app.register_blueprint(auth_bp,   url_prefix="/auth")
app.register_blueprint(worker_bp, url_prefix="/workers")
app.register_blueprint(health_bp, url_prefix="")
app.register_blueprint(protected_bp, url_prefix="")

# --- Flask 3 compatible table creation (run once at startup) ---
with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)
