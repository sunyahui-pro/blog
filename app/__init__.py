from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = '请先登录'
    
    from app.routes import main, post, auth
    app.register_blueprint(main.main)
    app.register_blueprint(post.bp)
    app.register_blueprint(auth.bp)
    
    with app.app_context():
        db.create_all()
    
    return app
