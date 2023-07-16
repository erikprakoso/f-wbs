from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config

db = SQLAlchemy()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Set the static folder for serving static files
    app.static_folder = 'static'

    # Initialize database
    db.init_app(app)

    # Create an instance of Migrate and associate it with your Flask application and database
    migrate = Migrate()
    migrate.init_app(app, db, directory='app//models/migrations')

    # Register blueprints
    from app.routes.auth import auth_bp
    from app.routes.project import project_bp
    from app.routes.sheet_name import sheet_name_bp
    from app.routes.wbs import wbs_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(project_bp)
    app.register_blueprint(sheet_name_bp)
    app.register_blueprint(wbs_bp)

    return app