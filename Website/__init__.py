from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

def create_app():
    app = Flask(__name__)
    app.config['SECRET KEY'] = 'airbus'

    return app


   