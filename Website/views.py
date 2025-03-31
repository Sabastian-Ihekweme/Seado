from flask import Blueprint, render_template
from flask_login import login_required, current_user

views = Blueprint('views', __name__)

#tutor views

@views.route('/tutor-dashboard')
@login_required
def tutor_dashboard():

    return render_template("tutor/tutor-dashboard.html")

@views.route('/tutor-details')
def tutor_details():
    return render_template("tutor/tutor-details.html")

@views.route('/tutor-bookings')
def tutor_bookings():
    return render_template("tutor/tutor-bookings.html")

@views.route('/tutor-make-post')
def tutor_make_post():
    return render_template("tutor/tutor-make-post.html")

@views.route('/tutor-chat')
def tutor_chat():
    return render_template("tutor/tutor-chat.html")

@views.route('/tutor-live-session')
def tutor_live_session():
     return render_template("tutor/tutor-live-session.html")

@views.route('/tutor-recent-chats')
def tutor_recent_chats():
    return render_template("tutor/tutor-recent-chats.html")

@views.route('/tutor-view-post')
def tutor_view_post():
    return render_template("tutor/tutor-view-post.html")

@views.route('/tutor-view-student')
def tutor_view_student():
    return render_template("tutor/tutor-view-student.html")



#student views

@views.route('/student-dashboard')
def student_dashboard():
    return "<h2>Student Dashboard</h2>"

@views.route('/student-details')
def student_details():
    return "<h2>Student Profile</h2>"

@views.route('/student-chat')
def student_chat():
    return "<h2>Chat<h2>"

@views.route('/student-invitations')
def student_invitations():
    return "<h2>Student Invitations</h2>"

@views.route('/student-live-session')
def student_live_session():
    return "<h2>Student Live Session</h2>"

@views.route('/student-live-session-end')
def student_live_session_end():
    return "<h2>Student Live Session End</h2>"

@views.route('/student-recent-chats')
def student_recent_chats():
    return "<h2>Student Recent Chats</h2>"

@views.route('/student-view-materials')
def student_view_materials():
    return "<h2>Student View Materials</h2>"

@views.route('/student-view-tutor')
def student_view_tutor():
    return "<h2>Student View Tutor</h2>"