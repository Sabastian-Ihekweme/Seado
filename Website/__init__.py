# Website/__init__.py

from flask import Flask, abort, flash, redirect, session, url_for, request, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
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
    app.config['UPLOAD_FOLDER'] = 'static/uploads'
    app.config['MATERIAL_UPLOAD_FOLDER'] = os.path.join(app.static_folder, 'uploads/materials')
    os.makedirs(app.config['MATERIAL_UPLOAD_FOLDER'], exist_ok=True)

    db.init_app(app)
    login_manager.login_view = 'auth.tutor_login'
    login_manager.init_app(app)

    from .models import Booking, Tutor, Student, Post  # <-- imported after db is set up

    @login_manager.user_loader
    def load_user(id):
        tutor = Tutor.query.get(int(id))
        if tutor:
            return tutor
        return None

    @app.context_processor
    def inject_user():
        return dict(tutor=current_user)

    from .auth import auth
    from .views import views

    app.register_blueprint(auth, url_prefix='')
    app.register_blueprint(views, url_prefix='')

    create_database(app)

    @app.route('/search', methods=['GET'])
    def search():
        query = request.args.get('q', '').strip()

        tutor_results = []
        post_results = []

        if query:
            tutor_results = Tutor.query.filter(Tutor.firstName.ilike(f"%{query}%")).all() 
            post_results = Post.query.filter(Post.content.ilike(f"%{query}%")).all()
        else:
            tutor_results = []
            post_results = Post.query.all()
        return render_template('student/student-dashboard.html', tutor_results=tutor_results, post_results=post_results, query=query)

    return app


def create_database(app):
    if not path.exists('Website/' + DB_NAME):
        with app.app_context():
            db.create_all()
        print('Database Created!')


    
