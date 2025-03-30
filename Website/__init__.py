from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from os import path
import os 

UPLOAD_FOLDER = 'Website/static/uploads'
ALLOWED_EXTENSTIONS = {'png','jpg', 'jpeg', 'gif', 'mp4', 'avi', 'mov', 'pdf', 'docx'}


db = SQLAlchemy()
DB_NAME = 'database.db'

def create_app():
    app = Flask(__name__)
    app.config['SECRET KEY'] = 'airbus'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    from .auth import auth
    from .views import views


    app.register_blueprint(auth, url_prefix='/auth')
    app.register_blueprint(views, url_prefix='')

    from .models import Tutor, Student
    create_database(app)

    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


    return app


def create_database(app):
    if not path.exists('Website/' + DB_NAME):
        with app.app_context():
            db.create_all()
        print('Database Created!')


   