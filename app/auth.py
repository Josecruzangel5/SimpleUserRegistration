from flask import Blueprint, render_template, request, redirect, url_for, flash, make_response
from app import db
from app.models import User, Session
from app.utils import hash_password, check_password, is_valid_password, is_valid_name
from datetime import datetime, timedelta
import uuid
from email_validator import validate_email, EmailNotValidError
from sqlalchemy.exc import IntegrityError

auth_bp = Blueprint('auth', __name__, url_prefix='/')

@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        return render_template('signup.html')
    
    email = request.form.get('email', '').strip()
    full_name = request.form.get('full_name', '').strip()
    password = request.form.get('password', '')
    
    # validate mail
    try:
        valid = validate_email(email)
        email = valid.email
    except EmailNotValidError:
        flash('invalid email.', 'danger')
        return render_template('signup.html'), 400
    
    # validate name
    valid_name, msg_name = is_valid_name(full_name)
    if not valid_name:
        flash(msg_name, 'danger')
        return render_template('signup.html'), 400
    
    # validate password
    valid_pass, msg_pass = is_valid_password(password)
    if not valid_pass:
        flash(msg_pass, 'danger')
        return render_template('signup.html'), 400
    
    # verify if email already exists
    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        flash('Email already in use', 'danger')
        return render_template('signup.html'), 409
    
    # hash password
    hashed = hash_password(password)
    
    # create user
    new_user = User(email=email, full_name=full_name, password_hash=hashed)
    db.session.add(new_user)
    
    try:
        db.session.commit()
        flash('Registration Successful!.', 'success')
        return redirect(url_for('auth.login'))
    except IntegrityError:
        db.session.rollback()
        flash('Error while saving user, try again', 'danger')
        return render_template('signup.html'), 500


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    
    # POST
    email = request.form.get('email', '').strip()
    password = request.form.get('password', '')
    
    # search user by email
    user = User.query.filter_by(email=email).first()
    if not user:
        flash('Invalid Credentials.', 'danger')
        return render_template('login.html'), 401
    
    now = datetime.utcnow()
    
    # Verify block
    if user.locked_until and user.locked_until > now:
        remaining = (user.locked_until - now).seconds // 60  # minutes
        flash(f'Account blocked for {remaining} minutes.', 'danger')
        return render_template('login.html'), 403
    
    # if block expired, reset counter
    if user.locked_until and user.locked_until < now:
        user.failed_attempts = 0
        user.locked_until = None
        db.session.commit()
    
    # verify password
    if check_password(password, user.password_hash):
        # Login succesful: reset tries and block
        user.failed_attempts = 0
        user.locked_until = None
        db.session.commit()
        
        # Eliminate previous session
        Session.query.filter_by(user_id=user.id).delete()
        
        # Create new session
        session_id = str(uuid.uuid4())
        new_session = Session(id=session_id, user_id=user.id, created_at=now, last_activity=now)
        db.session.add(new_session)
        db.session.commit()
        
        # Create response and establish cookie
        response = make_response(render_template('dashboard.html', full_name=user.full_name))
        response.set_cookie('session_id', session_id, httponly=True, samesite='Lax')
        return response
    else:
        # Login failed
        user.failed_attempts += 1
        if user.failed_attempts >= 3:
            user.locked_until = datetime.utcnow() + timedelta(hours=2)
            flash('Too many tries. Account locked for 2 hours.', 'danger')
        else:
            flash('Invalid Credentials.', 'danger')
        db.session.commit()
        return render_template('login.html'), 401


@auth_bp.route('/logout')
def logout():
    session_id = request.cookies.get('session_id')
    if session_id:
        session = Session.query.filter_by(id=session_id).first()
        if session:
            db.session.delete(session)
            db.session.commit()
    response = redirect(url_for('auth.login'))
    response.delete_cookie('session_id')
    flash('Logged Out.', 'info')
    return response