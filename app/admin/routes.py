from flask import render_template, current_app, request, flash, redirect, url_for, session
from app.admin import admin_bp
from app.database.SchoolManagementSystem import SchoolManagementSystem
from werkzeug.security import generate_password_hash

@admin_bp.before_app_request
def before_request():
    global db
    db = SchoolManagementSystem(current_app.config['DB_CONFIG'])

@admin_bp.route('/dashboard')
def dashboard():
    return render_template('admin/dashboard.html')

# View Users
@admin_bp.route('/users')
def users():
    role = request.args.get('role', 'student')
    page = int(request.args.get('page', 1))
    limit = 10
    offset = (page - 1) * limit
    users = db.get_users_by_role(role, limit, offset)
    return render_template('admin/users.html', users=users, current_role=role)

# Add User
@admin_bp.route('/add-user', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        username = request.form.get('username')
        name = request.form.get('name')
        email = request.form.get('email')
        role = request.form.get('role')
        password = request.form.get('password')
        
        password_hash = generate_password_hash(password)
        if db.create_user(username, name, email, role, password_hash):
            flash('User created successfully', 'success')
            return redirect(url_for('admin.users', role=role))
        
        flash('Error creating user', 'danger')
    return render_template('admin/users.html')

# Edit User
@admin_bp.route('/edit-user/<username>', methods=['GET', 'POST'])
def edit_user(username):
    # Retrieve the user from the database
    user = db.get_user_by_username(username)
    
    if not user:
        flash('User not found', 'danger')
        return redirect(url_for('admin.users'))
    
    if request.method == 'POST':
        # Get form data
        name = request.form.get('name')
        email = request.form.get('email')
        role = request.form.get('role')
        
        # Password is optional - only update if provided
        password = request.form.get('password')
        
        # Prepare update data
        update_data = {
            'name': name,
            'email': email,
            'role': role
        }
        
        # If password is provided, hash it
        if password:
            update_data['password_hash'] = generate_password_hash(password)
        
        # Attempt to update user
        if db.update_user(username, update_data):
            flash('User updated successfully', 'success')
            return redirect(url_for('admin.users', role=role))
        
        flash('Error updating user', 'danger')
    
    return render_template('admin/edit_user.html', user=user)

# Delete User
@admin_bp.route('/delete-user/<username>', methods=['POST'])
def delete_user(username):
    # Retrieve the user's role before deleting for redirecting
    user = db.get_user_by_username(username)
    
    if not user:
        flash('User not found', 'danger')
        return redirect(url_for('admin.users'))
    
    if db.delete_user(username):
        flash('User deleted successfully', 'success')
        return redirect(url_for('admin.users', role=user['role']))
    
    flash('Error deleting user', 'danger')
    return redirect(url_for('admin.users'))



# Class Management Routes
@admin_bp.route('/classes')
def classes():
    classes = db.get_all_classes()
    teachers = db.get_all_teachers()
    return render_template('admin/classes.html', classes=classes, teachers=teachers)

@admin_bp.route('/add-class', methods=['POST'])
def add_class():
    class_name = request.form.get('class_name')
    coordinator_id = request.form.get('coordinator_id')
    
    if db.create_class(class_name, coordinator_id):
        flash('Class created successfully', 'success')
    else:
        flash('Error creating class', 'danger')
    
    return redirect(url_for('admin.classes'))

@admin_bp.route('/edit-class/<int:class_id>', methods=['POST'])
def edit_class(class_id):
    class_name = request.form.get('class_name')
    coordinator_id = request.form.get('coordinator_id')
    
    if db.update_class(class_id, class_name, coordinator_id):
        flash('Class updated successfully', 'success')
    else:
        flash('Error updating class', 'danger')
    
    return redirect(url_for('admin.classes'))

@admin_bp.route('/delete-class/<int:class_id>', methods=['POST'])
def delete_class(class_id):
    if db.delete_class(class_id):
        flash('Class deleted successfully', 'success')
    else:
        flash('Error deleting class', 'danger')
    
    return redirect(url_for('admin.classes'))


# Subject Management Routes
@admin_bp.route('/subjects')
def subjects():
    subjects = db.get_all_subjects()
    classes = db.get_all_classes()
    teachers = db.get_all_teachers()
    return render_template('admin/subjects.html', 
                         subjects=subjects, 
                         classes=classes, 
                         teachers=teachers)

@admin_bp.route('/add-subject', methods=['POST'])
def add_subject():
    subject_name = request.form.get('subject_name')
    class_id = request.form.get('class_id')
    teacher_id = request.form.get('teacher_id')
    
    if db.create_subject(subject_name, class_id, teacher_id):
        flash('Subject created successfully', 'success')
    else:
        flash('Error creating subject', 'danger')
    
    return redirect(url_for('admin.subjects'))

@admin_bp.route('/edit-subject/<int:subject_id>', methods=['POST'])
def edit_subject(subject_id):
    subject_name = request.form.get('subject_name')
    class_id = request.form.get('class_id')
    teacher_id = request.form.get('teacher_id')
    
    if db.update_subject(subject_id, subject_name, class_id, teacher_id):
        flash('Subject updated successfully', 'success')
    else:
        flash('Error updating subject', 'danger')
    
    return redirect(url_for('admin.subjects'))

@admin_bp.route('/delete-subject/<int:subject_id>', methods=['POST'])
def delete_subject(subject_id):
    if db.delete_subject(subject_id):
        flash('Subject deleted successfully', 'success')
    else:
        flash('Error deleting subject', 'danger')
    
    return redirect(url_for('admin.subjects'))


# Time Table Management Routes
@admin_bp.route('/timetable')
def timetable():
    class_id = request.args.get('class_id', type=int)
    classes = db.get_all_classes()
    subjects = db.get_all_subjects()
    teachers = db.get_all_teachers()
    
    if class_id:
        timetable_entries = db.get_timetable_by_class(class_id)
    else:
        timetable_entries = db.get_all_timetable_entries()
    
    return render_template('admin/timetable.html',
                         timetable_entries=timetable_entries,
                         classes=classes,
                         subjects=subjects,
                         teachers=teachers,
                         selected_class=class_id,
                         days=['Monday', 'Tuesday', 'Wednesday', 
                              'Thursday', 'Friday', 'Saturday'])

@admin_bp.route('/add-timetable', methods=['POST'])
def add_timetable():
    class_id = request.form.get('class_id', type=int)
    subject_id = request.form.get('subject_id', type=int)
    teacher_id = request.form.get('teacher_id', type=int)
    day = request.form.get('day')
    start_time = request.form.get('start_time')
    end_time = request.form.get('end_time')
    
    if db.create_timetable_entry(class_id, subject_id, teacher_id, 
                                day, start_time, end_time):
        flash('Timetable entry created successfully', 'success')
    else:
        flash('Error creating timetable entry. Please check for schedule conflicts.', 'danger')
    
    return redirect(url_for('admin.timetable', class_id=class_id))

@admin_bp.route('/edit-timetable/<int:timetable_id>', methods=['POST'])
def edit_timetable(timetable_id):
    class_id = request.form.get('class_id', type=int)
    subject_id = request.form.get('subject_id', type=int)
    teacher_id = request.form.get('teacher_id', type=int)
    day = request.form.get('day')
    start_time = request.form.get('start_time')
    end_time = request.form.get('end_time')
    
    if db.update_timetable_entry(timetable_id, class_id, subject_id,
                                teacher_id, day, start_time, end_time):
        flash('Timetable entry updated successfully', 'success')
    else:
        flash('Error updating timetable entry. Please check for schedule conflicts.', 'danger')
    
    return redirect(url_for('admin.timetable', class_id=class_id))

@admin_bp.route('/delete-timetable/<int:timetable_id>', methods=['POST'])
def delete_timetable(timetable_id):
    class_id = request.form.get('class_id', type=int)
    
    if db.delete_timetable_entry(timetable_id):
        flash('Timetable entry deleted successfully', 'success')
    else:
        flash('Error deleting timetable entry', 'danger')
    
    return redirect(url_for('admin.timetable', class_id=class_id))


# Exam Management Routes
@admin_bp.route('/exams')
def exams():
    class_id = request.args.get('class_id', type=int)
    classes = db.get_all_classes()
    
    if class_id:
        exams = db.get_exams_by_class(class_id)
    else:
        exams = db.get_all_exams()
    
    return render_template('admin/exams.html',
                         exams=exams,
                         classes=classes,
                         selected_class=class_id)

@admin_bp.route('/add-exam', methods=['POST'])
def add_exam():
    exam_name = request.form.get('exam_name')
    class_id = request.form.get('class_id', type=int)
    exam_date = request.form.get('exam_date')
    
    if db.create_exam(exam_name, class_id, exam_date):
        flash('Exam created successfully', 'success')
    else:
        flash('Error creating exam', 'danger')
    
    return redirect(url_for('admin.exams', class_id=class_id))

@admin_bp.route('/edit-exam/<int:exam_id>', methods=['POST'])
def edit_exam(exam_id):
    exam_name = request.form.get('exam_name')
    class_id = request.form.get('class_id', type=int)
    exam_date = request.form.get('exam_date')
    
    if db.update_exam(exam_id, exam_name, class_id, exam_date):
        flash('Exam updated successfully', 'success')
    else:
        flash('Error updating exam', 'danger')
    
    return redirect(url_for('admin.exams', class_id=class_id))

@admin_bp.route('/delete-exam/<int:exam_id>', methods=['POST'])
def delete_exam(exam_id):
    class_id = request.form.get('class_id', type=int)
    
    if db.delete_exam(exam_id):
        flash('Exam deleted successfully', 'success')
    else:
        flash('Error deleting exam', 'danger')
    
    return redirect(url_for('admin.exams', class_id=class_id))



