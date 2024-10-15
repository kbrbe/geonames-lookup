# app/__init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

# Initialize the database
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    CORS(app)  # Enable CORS for all routes
    app.config.from_object('config.DevelopmentConfig')  # Load configurations from config.py
    db.init_app(app)

    # Import and register routes
    with app.app_context():
        from .routes import register_routes
        register_routes(app)

    return app

