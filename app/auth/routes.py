from flask import render_template, current_app, request, session, flash, redirect, url_for
from app.auth import auth_bp
from app.database.SchoolManagementSystem import SchoolManagementSystem
from werkzeug.security import check_password_hash

@auth_bp.before_app_request
def before_request():
    global db
    db = SchoolManagementSystem(current_app.config['DB_CONFIG'])
    

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = db.get_user_by_username(username)
        if user and check_password_hash(user['password_hash'], password):
            session['user_id'] = user['user_id']
            session['user_role'] = user['role']
            session['user_name'] = user['name']
            flash('Login successful!', 'success')
            if user['role'] == 'admin':
                return redirect(url_for('admin.dashboard'))
            elif user['role'] == 'teacher':
                return redirect(url_for('teacher.dashboard'))
            else:
                return redirect(url_for('student.dashboard'))
        
        flash('Invalid username or password', 'danger')

    return render_template('auth/login.html')


@auth_bp.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out', 'info')
    return redirect(url_for('auth.login'))