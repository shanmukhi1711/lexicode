from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash
from models import db, User
from datetime import datetime, timedelta

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
        
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        user = User.query.filter_by(email=email).first()
        
        if user:
            if user.locked_until and user.locked_until > datetime.utcnow():
                flash('Account locked. Please try again later.', 'danger')
                return render_template('login.html')
                
            if user.check_password(password):
                user.failed_logins = 0
                user.locked_until = None
                db.session.commit()
                login_user(user)
                return redirect(url_for('main.dashboard'))
            else:
                user.failed_logins += 1
                if user.failed_logins >= 5:
                    user.locked_until = datetime.utcnow() + timedelta(minutes=1)
                db.session.commit()
                flash('Invalid email or password.', 'danger')
        else:
            flash('Invalid email or password.', 'danger')
            
    return render_template('login.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
        
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        if len(password) < 8:
            flash('Password must be at least 8 characters.', 'danger')
            return render_template('register.html')
            
        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email address already exists', 'danger')
            return render_template('register.html')
            
        new_user = User(email=email)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        
        flash('Registration successful. Please log in.', 'success')
        return redirect(url_for('auth.login'))
        
    return render_template('register.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
