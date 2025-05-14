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
    created_at = db.Column(db.DateTime, default=datetime.utcnow)



#Table for posts
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    tags = db.Column(db.String(200))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    thumbnail = db.Column(db.String(200))
    files = db.Column(db.Text)

    tutor_id = db.Column(db.Integer, db.ForeignKey('tutor.id'), nullable=False)
    tutor = db.relationship('Tutor', backref='posts', lazy=True)

#Table for material
class Material(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(20), nullable=False)  # 'video', 'pdf', etc.
    filename = db.Column(db.String(100), nullable=False)
    upload_date = db.Column(db.DateTime, default=datetime.utcnow)
    tutor_id = db.Column(db.Integer, db.ForeignKey('tutor.id'))
    


#Table for bookings
class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    tutor_id = db.Column(db.Integer, db.ForeignKey('tutor.id'), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    accepted = db.Column(db.Boolean, default=False)
    whiteboard_id = db.Column(db.String(100), nullable=True)
    invited = db.Column(db.Boolean, default=False)
    room = db.Column(db.String(100), nullable=True)

    student = db.relationship('Student', backref='bookings')
    tutor = db.relationship('Tutor', backref='bookings')

