from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from .models import Tutor, Student, Post
from . import db
from werkzeug.security import generate_password_hash
from werkzeug.utils import secure_filename
from Website import allowed_file
import os

auth = Blueprint('auth', __name__)

@auth.route('/tutor-signup', methods=['GET', 'POST'])
def tutor_signup():
    if request.method == 'POST':
        firstName = request.form.get('firstName')
        lastName = request.form.get('lastName')
        qualification = request.form.get('qualification')
        course = request.form.get('course')
        email = request.form.get('email')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        #profile picture handling
        profilePicture = request.files.get('profilePicture')
        file_path = None

        if profilePicture and allowed_file(profilePicture.filename):
            filename = secure_filename(profilePicture.filename)
            file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            profilePicture.save(file_path)
            

        existing_tutor = Tutor.query.filter_by(email=email).first()
        hashedPassword = generate_password_hash(password1, method='pbkdf2:sha256')

        if existing_tutor:
            flash(f'Account already exists! Please <a class="flash-link" href="{url_for("auth.tutor_login")}">log in</a>.', "error")
        elif password1 != password2:
            flash('Passwords do not match!', category="error")
            return redirect(url_for('auth.tutor_signup'))
        elif len(password1) < 7:
            flash('Password must be longer than 7 characters!', category="error")
        else:
            #add new user to database
            new_tutor = Tutor (
                firstName = firstName,
                lastName = lastName,
                qualification = qualification,
                course = course,
                email = email,
                password = hashedPassword,
                profilePicture = file_path
            )

            db.session.add(new_tutor)
            db.session.commit()


            flash(f'Account created successfully! Please <a class="flash-link" href="{url_for("auth.tutor_login")}">log in</a>.', "success")
           

    return render_template("tutor/tutor-signup.html")

@auth.route('/tutor-login')
def tutor_login():
    return "<h2>Tutor login</h2>"

@auth.route('/',  methods=['GET', 'POST'])
def student_signup():
    if request.method == 'POST':
        firstName = request.form.get('firstName')
        lastName = request.form.get('lastName')
        school = request.form.get('school')
        levelOfStudy = request.form.get('level-of-study')
        year = request.form.get('year')
        email = request.form.get('email')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        #profile picture handling
        profilePicture = request.files.get('profilePicture')
        file_path = None

        if profilePicture and allowed_file(profilePicture.filename):
            filename = secure_filename(profilePicture.filename)
            file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            profilePicture.save(file_path)
            

        existing_student = Student.query.filter_by(email=email).first()
        hashedPassword = generate_password_hash(password1, method='pbkdf2:sha256')

        if existing_student:
            flash(f'Account already exists! Please <a class="flash-link" href="{url_for("auth.student_login")}">log in</a>.', "error")
        elif password1 != password2:
            flash('Passwords do not match!', category="error")
            return redirect(url_for('auth.student_signup'))
        elif len(password1) < 7:
            flash('Password must be longer than 7 characters!', category="error")
        else:
            #add new user to database
            new_student = Student (
                firstName = firstName,
                lastName = lastName,
                school = school,
                levelOfStudy = levelOfStudy,
                year = year,
                email = email,
                password = hashedPassword,
                profilePicture = file_path
            )

            db.session.add(new_student)
            db.session.commit()


            flash(f'Account created successfully! Please <a class="flash-link" href="{url_for("auth.student_login")}">log in</a>.', "success")

    return render_template("student/student-signup.html")


@auth.route('/student-login')
def student_login():
    return "<h2>Student login</h2>"

@auth.route('/tutor-logout')
def tutor_logout():
    return "<h2>Tutor logout</h2>"

@auth.route('/student-logout')
def student_logout():
    return "<h2>Student logout</h2>"