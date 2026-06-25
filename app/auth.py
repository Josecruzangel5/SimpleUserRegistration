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
        flash('Error while saving user, try agaain', 'danger')
        return render_template('signup.html'), 500