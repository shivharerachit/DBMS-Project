from flask import render_template, current_app
from app.student import student_bp
from app.database.SchoolManagementSystem import SchoolManagementSystem

@student_bp.before_app_request
def before_request():
    global db
    db = SchoolManagementSystem(current_app.config['DB_CONFIG'])

@student_bp.route('/dashboard')
def dashboard():
    return render_template('student/dashboard.html')

@student_bp.route('/timetable')
def timetable():
    student_id = 1  # Get from session
    timetable = db.get_student_timetable(student_id)
    return render_template('student/timetable.html', timetable=timetable)

@student_bp.route('/results')
def results():
    student_id = 1  # Get from session
    results = db.get_student_performance(student_id)
    return render_template('student/results.html', results=results)