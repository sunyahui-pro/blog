from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config
from datetime import datetime

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = '请先登录'

    # Add user_loader for Flask-Login
    from app.models import User
    @login_manager.user_loader
    def load_user(user_id):
        # Simple user loader for single user system
        if user_id == '1':
            return User(id=1, username='feizi')
        return None

    # Add context processor for current_year
    @app.context_processor
    def inject_globals():
        return dict(current_year=datetime.now().year)

    from app.routes.main import main
    from app.routes.post import bp as post_bp
    from app.routes.auth import bp as auth_bp
    app.register_blueprint(main)
    app.register_blueprint(post_bp)
    app.register_blueprint(auth_bp)

    with app.app_context():
        db.create_all()

    return app
