# app/views.py (your existing view file)
from flask import render_template, redirect, session, url_for, flash
from app.controllers.forms import RegistrationForm, LoginForm
from . import user_bp as user
from app.controllers.user import UserController

user_controller = UserController()

@user.route('/register', methods=['GET', 'POST'])
def register():
    try:
        form = RegistrationForm()
        if form.validate_on_submit():
            user = user_controller.create_user(
                form.first_name.data,
                form.last_name.data,
                form.email.data,
                form.password.data,
                form.address.data,
                form.dob.data,
                form.gender.data,
                form.is_admin.data
            )
            flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('user.login')) 
        return render_template('newUser.html', form=form)
    except Exception as error:
        flash(error, 'danger')
        return render_template('newUser.html', form=form)

@user.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = user_controller.login_user(form.email.data, form.password.data)
        if user and not user.is_admin:
            flash('Logged in successfully', 'success')
            session['user_id'] = user.id  
            session['logged_in'] = True  
            return redirect(url_for('main.home'))
        flash('Invalid credentials', 'danger')
    return render_template('login.html', form=form)

@user.route('/admin_login', methods=['GET','POST'])
def admin_login():
    print("Here")
    form = LoginForm()
    if form.validate_on_submit():
        user = user_controller.login_user(form.email.data, form.password.data)
        if  user and user.is_admin:
            flash('Logged in successfully', 'success')
            session['user_id'] = user.id  
            session['logged_in'] = True  
            session['is_admin'] = True  
            return redirect(url_for('main.home'))
        flash('Invalid credentials', 'danger')
    return render_template('adminLogin.html', form=form)

@user.route('/logout', methods=['GET', 'POST'])
def logout():
    session.clear()  # Clear all session data
    flash('You have been logged out successfully.', 'success')
    return redirect(url_for('user.login'))

@user.route('/admin_panel', methods=['GET', 'POST'])
def admin_panel():
    return render_template("adminPanel.html")

@user.route('/get_all_students', methods=['GET'])
def get_all_students():
    users = user_controller.get_all_users(False)
    if not users:
        flash('Users not found', 'warning')
        
    return render_template('viewStudents.html', users=users)