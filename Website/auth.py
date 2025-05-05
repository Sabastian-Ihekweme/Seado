from flask import Blueprint, session, render_template, request, redirect, url_for, flash, current_app
from .models import Tutor, Student, Post
from .models import db
from flask_login import login_user, LoginManager, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
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
        filename = None  # Default is None

        if profilePicture and allowed_file(profilePicture.filename):
            filename = secure_filename(profilePicture.filename)
            upload_folder = current_app.config['UPLOAD_FOLDER']
            profile_pic_path = os.path.join(upload_folder, filename)
            profilePicture.save(profile_pic_path)
            

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
                profilePicture = filename if filename else "default.jpg"
            )

            db.session.add(new_tutor)
            db.session.commit()


            flash(f'Account created successfully! Please <a class="flash-link" href="{url_for("auth.tutor_login")}">log in</a>.', "success")
    
    return  render_template('tutor/tutor-signup.html')



@auth.route('/', methods=['GET', 'POST'])
def tutor_login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        tutor = Tutor.query.filter_by(email=email).first()

        if tutor and tutor.password:
            if check_password_hash(tutor.password, password):
                login_user(tutor)
                session['tutor_id'] = tutor.id
                return redirect(url_for('views.tutor_dashboard'))
                flash("Login successful!", "success")
            else:
                flash("Incorrect password. Please try again.", category="error")
        else: 
            flash("Email not found. Please try again", category="error")

    return render_template('tutor/tutor-login.html')

@auth.route('/student-signup',  methods=['GET', 'POST'])
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


@auth.route('/student-login', methods=['GET', 'POST'])
def student_login():
    if request.method == 'POST':

        email = request.form.get('email')
        password = request.form.get('password')

        # (authenticate the student)
        student = Student.query.filter_by(email=email).first()
        if student and check_password_hash(student.password, password):
            session['student_id'] = student.id  # ✅ THIS IS ESSENTIAL
            login_user(student)
            flash("Logged in successfully!", "success")
            return redirect(url_for('views.student_dashboard'))
        else:
            flash("Invalid credentials.", "error")

    return render_template('student/student-login.html')


@auth.route('/tutor-logout')
def tutor_logout():
    logout_user()

    return redirect(url_for('auth.tutor_login'))

@auth.route('/student-logout')
def student_logout():
    logout_user()


    return redirect(url_for('auth.student_login'))