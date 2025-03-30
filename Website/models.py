from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from datetime import datetime



#Table for tutors
class Tutor(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    firstName = db.Column(db.String(150), nullable=False)
    lastName = db.Column(db.String(150), nullable=False)
    qualification = db.Column(db.String(150), nullable=True)
    course = db.Column(db.String(150), nullable=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    profilePicture = db.Column(db.String(255), nullable=True)


#Table for students
class Student(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    firstName = db.Column(db.String(150), nullable=False)
    lastName = db.Column(db.String(150), nullable=False)
    school = db.Column(db.String(150), nullable=False)
    levelOfStudy = db.Column(db.String(150), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    profilePicture = db.Column(db.String(255), nullable=True)


#Table for posts
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tutor_id = db.Column(db.Integer, db.ForeignKey('tutor.id'), nullable=False)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=True)
    image = db.Column(db.String(255), nullable=True)
    video = db.Column(db.String(255), nullable=True)
    document = db.Column(db.String(255), nullable=True)
    thumbnail = db.Column(db.String(255), nullable=True)
    subjectTag = db.Column(db.String(150), nullable=True)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    tutor = db.relationship('Tutor', backref=db.backref('posts', lazy=True))