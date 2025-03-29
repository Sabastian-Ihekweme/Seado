from flask import Blueprint, render_template

views = Blueprint('views', __name__)

#tutor views

@views.route('/tutor-dashboard')
def tutor_dashboard():
    return "<h2>Tutor Dashboard</h2>"

@views.route('/tutor-details')
def tutor_details():
    return "<h2>Tutor Details</h2>"

@views.route('/tutor-bookings')
def tutor_bookings():
    return "<h2>Tutor Bookings</h2>"

@views.route('/tutor-make-post')
def tutor_make_post():
    return "<h2>Post</h2>"

@views.route('/tutor-chat')
def tutor_chat():
    return "<h2>Tutor Chat</h2>"

@views.route('/tutor-live-session')
def tutor_live_session():
    return "<h2>Tutor Live Session</h2>"

@views.route('/tutor-recent-chats')
def tutor_recent_chats():
    return "<h2>Tutor Recent Chats</h2>"

@views.route('/tutor-view-post')
def tutor_view_post():
    return "<h2>Tutor View Post</h2>"

@views.route('/tutor-view-student')
def tutor_view_student():
    return "<h2>Tutor View Student</h2>"



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