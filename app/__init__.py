"""Initialize Flask application"""
from flask import Flask
from config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Landing Page Blueprint
    from app.main import main_bp
    app.register_blueprint(main_bp)

    from app.auth import auth_bp
    app.register_blueprint(auth_bp)

    from app.admin import admin_bp
    app.register_blueprint(admin_bp)

    from app.teacher import teacher_bp
    app.register_blueprint(teacher_bp)

    from app.student import student_bp
    app.register_blueprint(student_bp)

    return app