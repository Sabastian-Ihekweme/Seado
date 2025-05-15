from flask import Blueprint, render_template, redirect, url_for,request, flash, current_app
from flask_login import login_required, current_user
from .models import Tutor, Student, Booking, Post
from .models import db
from flask import current_app
from .models import Material  
import os
from datetime import datetime
from werkzeug.security import generate_password_hash
from werkzeug.utils import secure_filename
import uuid

views = Blueprint('views', __name__)

def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'pdf', 'docx'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

#tutor views

@views.route('/tutor-dashboard')
@login_required
def tutor_dashboard():

    #Fetch posts made by tutor
    tutor_posts = Post.query.filter_by(tutor_id=current_user.id).order_by(Post.timestamp.desc()).all()

    return render_template("tutor/tutor-dashboard.html", tutor_posts=tutor_posts)

@views.route('/tutor-details', methods=['GET', 'POST'])
@login_required
def tutor_details():
        if request.method == 'POST':
            aboutMe = request.form.get('tutor-about-me').strip()

            tutor = current_user 

            tutor.aboutMe = aboutMe

        db.session.commit()
        flash('About Me updated successfully!', category="success")

        return render_template("tutor/tutor-details.html")

@views.route('/tutor-bookings')
def tutor_bookings():
    tutor_id = current_user.id
    bookings = Booking.query.filter_by(tutor_id=tutor_id).all()
    return render_template("tutor/tutor-bookings.html", bookings=bookings)

@views.route('/accept-booking/<int:booking_id>', methods=['POST'])
def accept_booking(booking_id):
    booking = Booking.query.get_or_404(booking_id)
    booking.accepted = True
    db.session.commit()
    flash("Booking accepted", "success")
    return redirect(url_for('views.tutor_bookings'))

@views.route('/invite-student/<int:booking_id>', methods=['POST'])
def invite_student(booking_id):
    booking = Booking.query.get_or_404(booking_id)
    booking.invited = True
    db.session.commit()
    flash("Student Invited", "success")
    return redirect(url_for('views.tutor_whiteboard_session'))


@views.route('/tutor-make-post', methods=['GET', 'POST'])
def tutor_make_post():
    if request.method == 'POST':
        upload_path = current_app.config['UPLOAD_FOLDER']
        content = request.form.get('content')
        tags = request.form.get('tags')
        thumbnail = request.files.get('thumbnail')
        files = request.files.getlist('file')

        if not content:
            flash("Content is required!", category="error")
            return redirect(request.url)

        thumbnail_filename = None
        if thumbnail and allowed_file(thumbnail.filename):
            thumbnail_filename = secure_filename(thumbnail.filename)
            thumbnail.save(os.path.join(upload_path, thumbnail_filename))

        
        uploaded_filenames=[]
        if files:
            for file in files:
                if file and allowed_file(file.filename):
                    filename = secure_filename(file.filename)

                    upload_path = os.path.join(current_app.root_path, 'static', 'uploads')
                    os.makedirs(upload_path, exist_ok=True)

                    file_path = os.path.join(upload_path, filename)
                    file.save(file_path)

                    uploaded_filenames.append(filename)
                

        files_string = ','.join(uploaded_filenames) if uploaded_filenames else ''  


        new_post = Post(
            content=content,
            tags=tags,
            thumbnail=thumbnail_filename,
            files=files_string,
            tutor_id=current_user.id
        )
        db.session.add(new_post)
        db.session.commit()

        flash("Post successfully created!", category="success")
        return redirect(url_for('views.tutor_dashboard'))


    return render_template("tutor/tutor-make-post.html")

@views.route('/tutor-chat')
def tutor_chat():
    return render_template("tutor/tutor-chat-ui.html")

@views.route('/tutor-live-session')
def tutor_live_session():
     return render_template("tutor/tutor-live-session.html")

@views.route('/tutor-recent-chats')
def tutor_recent_chats():
    return render_template("tutor/tutor-recent-chats.html")

@views.route('/tutor-view-post')
def tutor_view_post():
    return render_template("tutor/tutor-view-post.html")

@views.route('/tutor-view-student/<int:student_id>')
def tutor_view_student(student_id):
    student = Student.query.get_or_404(student_id)
    return render_template("tutor/tutor-view-student.html", student=student)

@views.route('/tutor-whiteboard-session')
def tutor_whiteboard_session():
    tutor_id = current_user.id
    bookings = Booking.query.filter_by(tutor_id=tutor_id, accepted=True).all()
    return render_template("tutor/tutor-whiteboard-session.html", bookings=bookings)


#Whiteboard Route
@views.route('/start_whiteboard')
@login_required
def start_whiteboard():
    whiteboard_url = ""  # Ideally generated/stored per session
    return render_template("tutor-live-session.html", whiteboard_url=whiteboard_url)


#student views

@views.route('/student-dashboard')
def student_dashboard():
    

    return render_template("student/student-dashboard.html", student=current_user, posts=Post)


@views.route('/student-details')
@login_required
def student_details():


    return render_template("student/student-details.html", student=current_user)

@views.route('/student-view-bookings')
def student_view_bookings():
    return render_template("student/student-view-bookings.html", student=current_user)

@views.route('/student-chat')
def student_chat():
    return render_template("student/student-chat-ui.html", student=current_user)

@views.route('/student-invitations')
def student_invitations():
    student_id = current_user.id
    bookings = Booking.query.filter_by(student_id=student_id, invited=True).all()

    return render_template("student/student-invitations.html", bookings=bookings, student=current_user)

@views.route('/student-live-session')
def student_live_session():
    return render_template("student/student-live-session.html", student=current_user)

@views.route('/student-live-session-end')
def student_live_session_end():
    return render_template("student/student-live-session-end.html", student=current_user)

@views.route('/student-recent-chats')
def student_recent_chats():
    return render_template("student/student-recent-chats.html", student=current_user)

@views.route('/student-view-materials/<int:post_id>')
def student_view_materials(post_id):
    post = Post.query.get_or_404(post_id)
    tutor = post.tutor

    return render_template("student/student-view-materials.html", student=current_user, post=post, tutor=tutor)

@views.route('/student-view-tutor/<int:tutor_id>', methods=['GET', 'POST'])
def student_view_tutor(tutor_id):
    tutor = Tutor.query.get_or_404(tutor_id)

    if request.method == 'POST':
        student_id = current_user.id
        tutor_id = Tutor.query.get_or_404(tutor_id)
        timestamp = datetime.now().date()

        existing_booking = Booking.query.filter_by(tutor_id=tutor.id, student_id=student_id).first()

        if existing_booking:
            flash(f'You have already booked this tutor', 'error')
        else:
            #add new booking to database
            new_booking = Booking (
                student_id = student_id,
                tutor_id = tutor.id,
                timestamp = timestamp
            )
            db.session.add(new_booking)
            db.session.commit()

            flash(f'Booking request sent successfully!', 'success')
            return redirect(url_for('views.student_dashboard'))
    
    return render_template("student/student-view-tutor.html", student=current_user, tutor=tutor)



@views.route('/materials/<int:material_id>')
def view_material(material_id):
    if not current_user.is_authenticated:
        return redirect(url_for('auth.tutor_login'))
    
    material = Material.query.get_or_404(material_id)
    return render_template('tutor_view_post.html',
                        material=material,
                        current_time=datetime.now().strftime("%H:%M"))

@views.route('/materials/<int:material_id>', methods=['DELETE'])
def delete_material(material_id):
    if not current_user.is_authenticated:
        return {'success': False, 'message': 'Unauthorized'}, 401
    
    material = Material.query.get_or_404(material_id)
    
    try:
        # Delete file
        file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], material.filename)
        if os.path.exists(file_path):
            os.remove(file_path)
        
        # Delete record
        db.session.delete(material)
        db.session.commit()
        
        return {'success': True, 'redirect': url_for('views.tutor_dashboard')}
    except Exception as e:
        return {'success': False, 'message': str(e)}, 500


student = Blueprint('student', __name__)

@student.route('/view-student/<int:student_id>')
@login_required
def view_student(student_id):
    student = Student.query.get(student_id)
    if not student:
        flash('Student not found', 'error')
        return redirect(url_for('views.dashboard'))
    
    return render_template('view_student.html', 
                         student=student,
                         current_user=current_user)

