from flask import Flask
from flask_cors import CORS
import os
from dotenv import load_dotenv
from .db import db, migrate
from .bcrypt import bcrypt
from app.models.task import Task
from app.models.goal import Goal
from app.models.user import User
from app.models.session import Session
from .routes import goal_routes
from .routes import task_routes
from .routes import user_routes
from .routes import session_routes

load_dotenv()


def create_app(config=None):
    app = Flask(__name__)
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
        "SQLALCHEMY_DATABASE_URI")

    if config:
        app.config.update(config)

    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    CORS(app,
         supports_credentials=True,
         )

    # Register Blueprints here
    app.register_blueprint(goal_routes.bp)
    app.register_blueprint(task_routes.bp)
    app.register_blueprint(user_routes.bp)
    app.register_blueprint(session_routes.bp)

    return app
