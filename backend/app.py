from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv

from config import Config
from database.db import db, migrate
from routes.auth import auth_bp
from routes.worker import worker_bp
from routes.client import client_bp


def create_app():
    load_dotenv()
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    JWTManager(app)
    CORS(app)

    app.register_blueprint(auth_bp)
    app.register_blueprint(worker_bp)
    app.register_blueprint(client_bp)

    @app.route("/")
    def health():
        return {"message": "RodLi API is running"}

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
