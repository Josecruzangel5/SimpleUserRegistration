from flask import Flask 
from flask_sqlalchemy import SQLAlchemy
from config import Config 

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    from app import models 

    from app.auth import auth_bp
    app.register_blueprint(auth_bp)

    from app.middlewares import session_middleware
    app.before_request(session_middleware)

    return app 