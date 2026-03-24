import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'blog-secret-key-2024'
    
    # SQLite 配置（和原版一致）
    basedir = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'blog.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'app/static/uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024
    
    # 管理员账号
    ADMIN_USERNAME = os.environ.get('ADMIN_USERNAME') or 'feizi'
    ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD') or 'feizi'
