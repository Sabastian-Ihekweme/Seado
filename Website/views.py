from flask import Blueprint, render_template

views = Blueprint('views', __name__)

@views.route('/tutor-dashboard')
def tutor_dashboard():
    return "<h2>Tutor Dashboard</h2>"

@views.route('/tutor-details')
def tutor_details():
    return "<h2>Tutor Details</h2>"

@views.route('/bookings')
def bookings():
    return "<h2>Bookings</h2>"

@views.route('/post')
def bookings():
    return "<h2>Post</h2>"

@views.route('/student-dashboard')
def student_dashboard():
    return "<h2>Student Dashboard</h2>"

@views.route('/student-profile')
def student_profile():
    return "<h2>Student Profile</h2>"

@views.route('/chat')
def student_profile():
    return "<h2>Chat<h2>"