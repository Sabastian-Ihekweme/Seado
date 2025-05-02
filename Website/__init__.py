# Website/__init__.py

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user
from os import path
import os

db = SQLAlchemy()
login_manager = LoginManager()
DB_NAME = 'database.db'
ALLOWED_EXTENSIONS = {'png','jpg', 'jpeg', 'gif', 'mp4', 'avi', 'mov', 'pdf', 'docx'}

UPLOAD_FOLDER = os.path.join(os.getcwd(), 'static/uploads/profile-pics')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'airbus'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.config['MATERIAL_UPLOAD_FOLDER'] = os.path.join(app.static_folder, 'uploads/materials')
    os.makedirs(app.config['MATERIAL_UPLOAD_FOLDER'], exist_ok=True)

    db.init_app(app)
    login_manager.login_view = 'auth.tutor_login'
    login_manager.init_app(app)

    from .models import Tutor, Student  # <-- imported after db is set up

    @login_manager.user_loader
    def load_user(id):
        return Tutor.query.get(int(id)) or Student.query.get(int(id))

    @app.context_processor
    def inject_user():
        return dict(tutor=current_user)

    from .auth import auth
    from .views import views

    app.register_blueprint(auth, url_prefix='')
    app.register_blueprint(views, url_prefix='')

    create_database(app)

    return app


def create_database(app):
    if not path.exists('Website/' + DB_NAME):
        with app.app_context():
            db.create_all()
        print('Database Created!')
