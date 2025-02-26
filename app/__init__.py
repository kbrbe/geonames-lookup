# app/__init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_caching import Cache
import logging

# Initialize the database
db = SQLAlchemy()
cache = Cache()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_app():
    app = Flask(__name__)
    CORS(app)  # Enable CORS for all routes
    app.config.from_object('config.ProductionConfig')  # Load configurations from config.py
    db.init_app(app)
    cache.init_app(app)


    # Import and register routes
    with app.app_context():
        from .routes import register_routes
        register_routes(app)

    return app

