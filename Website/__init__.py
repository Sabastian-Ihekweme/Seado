from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user
from os import path
from werkzeug.utils import secure_filename
from flask import current_app
import os 

UPLOAD_FOLDER = os.path.join(os.getcwd(), 'static', 'uploads', 'profile-pics')
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
    print("Created upload folder:", UPLOAD_FOLDER)
ALLOWED_EXTENSIONS = {'png','jpg', 'jpeg', 'gif', 'mp4', 'avi', 'mov', 'pdf', 'docx'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


db = SQLAlchemy()
DB_NAME = 'database.db'
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'airbus'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
    db.init_app(app)

    from .auth import auth
    from .views import views


    app.register_blueprint(auth, url_prefix='') 
    app.register_blueprint(views, url_prefix='')

    from .models import Tutor, Student


    create_database(app)

    login_manager=LoginManager()
    login_manager.login_view = 'auth.tutor_login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return Tutor.query.get(int(id)) or Student.query.get(int(id))
    
    
    @app.context_processor
    def inject_user():
        return dict(tutor=current_user)


    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

    from .models import Tutor

    def load_user(user_id):
        return Tutor.query.get(int(user_id))

    return app







def create_database(app):
    if not path.exists('Website/' + DB_NAME):
        with app.app_context():
            db.create_all()
        print('Database Created!')





   