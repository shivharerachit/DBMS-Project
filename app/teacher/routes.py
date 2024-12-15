from flask import render_template, current_app, session, request, flash
from app.teacher import teacher_bp
from app.database.SchoolManagementSystem import SchoolManagementSystem

@teacher_bp.before_app_request
def before_request():
    global db
    db = SchoolManagementSystem(current_app.config['DB_CONFIG'])

@teacher_bp.route('/dashboard')
def dashboard():
    teacher_id = session.get('user_id')
    classes = db.get_teacher_classes(teacher_id)
    return render_template('teacher/dashboard.html', classes=classes)

@teacher_bp.route('/schedule')
def schedule():
    teacher_id = session.get('user_id')
    schedule = db.get_teacher_schedule(teacher_id)
    return render_template('teacher/schedule.html', schedule=schedule)

@teacher_bp.route('/mark-attendance', methods=['GET', 'POST'])
def mark_attendance():
    teacher_id = session.get('user_id')
    classes = db.get_teacher_classes(teacher_id)
    if request.method == 'POST':
        student_id = request.form.get('student_id')
        class_id = request.form.get('class_id')
        status = request.form.get('status')
        
        if db.mark_student_attendance(student_id, class_id, status):
            flash('Attendance marked successfully', 'success')
        else:
            flash('Error marking attendance', 'danger')
    
    selected_class = request.args.get('class_id')
    students = []
    if selected_class:
        students = db.get_class_students(selected_class)
            
    return render_template('teacher/mark_attendance.html', 
                         classes=classes, 
                         students=students,
                         selected_class=selected_class)




@teacher_bp.route('/add-result', methods=['GET', 'POST'])
def add_result():
    teacher_id = session.get('user_id')
    classes = db.get_teacher_classes(teacher_id)
    
    if request.method == 'POST':
        student_id = request.form.get('student_id')
        class_id = request.form.get('class_id')
        subject_id = request.form.get('subject_id')
        marks_obtained = request.form.get('marks_obtained')
        max_marks = request.form.get('max_marks')
        
        if db.add_result(student_id, class_id, subject_id, marks_obtained, max_marks):
            flash('Result added successfully', 'success')
        else:
            flash('Error adding result', 'danger')
    
    selected_class = request.args.get('class_id')
    students = []
    if selected_class:
        students = db.get_class_students(selected_class)
            
    return render_template('teacher/add_result.html',
                         classes=classes,
                         students=students,
                         selected_class=selected_class)