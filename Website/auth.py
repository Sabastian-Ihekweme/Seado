from flask import Blueprint, render_template

auth = Blueprint('auth', __name__)

@auth.route('/tutor-signup')
def tutor_signup():
    return render_template("tutor/tutor-signup.html")

@auth.route('/tutor-login')
def tutor_login():
    return "<h2>Tutor login</h2>"

@auth.route('/student-signup')
def student_signup():
    return "<h2>Student Signup</h2>" 

@auth.route('/student-login')
def student_login():
    return "<h2>Student login</h2>"

@auth.route('/tutor-logout')
def tutor_logout():
    return "<h2>Tutor logout</h2>"

@auth.route('/student-logout')
def student_logout():
    return "<h2>Student logout</h2>"