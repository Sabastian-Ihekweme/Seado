from flask import Blueprint, render_template, redirect, url_for,request, flash
from flask_login import login_required, current_user
from .models import Tutor, Student, Booking
from .models import db
from flask import current_app
from .models import Material  
import os
from datetime import datetime
from werkzeug.security import generate_password_hash

views = Blueprint('views', __name__)

#tutor views

@views.route('/tutor-dashboard')
@login_required
def tutor_dashboard():

    return render_template("tutor/tutor-dashboard.html")

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


@views.route('/tutor-make-post')
def tutor_make_post():
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


#student views

@views.route('/student-dashboard')
def student_dashboard():
    if not current_user.is_authenticated:
        return redirect(url_for('auth.student_login'))

    return render_template("student/student-dashboard.html", student=current_user)


@views.route('/student-details')
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
    return render_template("student/student-invitations.html", student=current_user)

@views.route('/student-live-session')
def student_live_session():
    return render_template("student/student-live-session.html", student=current_user)

@views.route('/student-live-session-end')
def student_live_session_end():
    return render_template("student/student-live-session-end.html", student=current_user)

@views.route('/student-recent-chats')
def student_recent_chats():
    return render_template("student/student-recent-chats.html", student=current_user)

@views.route('/student-view-materials')
def student_view_materials():
    return render_template("student/student-view-materials.html", student=current_user)

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