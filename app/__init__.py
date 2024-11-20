from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config

db = SQLAlchemy()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize Flask extensions
    db.init_app(app)

    # Import and register blueprints
    from app.api.roles import bp as roles_bp
    app.register_blueprint(roles_bp, url_prefix='/api')

    from app.api.users import bp as users_bp
    app.register_blueprint(users_bp, url_prefix='/api')

    from app.api.courses import bp as courses_bp
    app.register_blueprint(courses_bp, url_prefix='/api')

    from app.api.role_courses import bp as role_courses_bp
    app.register_blueprint(role_courses_bp, url_prefix='/api')

    from app.api.user_courses import bp as user_courses_bp
    app.register_blueprint(user_courses_bp, url_prefix='/api')

    # Create database tables
    with app.app_context():
        db.create_all()

    return app