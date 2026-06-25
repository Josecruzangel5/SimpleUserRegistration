from flask import request, redirect, url_for, make_response, flash
from app import db
from app.models import Session
from datetime import datetime
import config

def session_middleware():
    
   
    public_paths = ['/login', '/signup', '/static']
    if request.path in public_paths or request.path.startswith('/static/'):
        return None  
    
    
    session_id = request.cookies.get('session_id')
    if not session_id:
        return redirect(url_for('auth.login'))
    
    
    session_record = Session.query.filter_by(id=session_id).first()
    if not session_record:
        response = make_response(redirect(url_for('auth.login')))
        response.delete_cookie('session_id')
        return response
    
    
    now = datetime.utcnow()
    time_diff = (now - session_record.last_activity).total_seconds() / 60  
    
    if time_diff > config.Config.SESSION_TIMEOUT_MINUTES:
        db.session.delete(session_record)
        db.session.commit()
        response = make_response(redirect(url_for('auth.login')))
        response.delete_cookie('session_id')
        flash('Session expired because of inactivity.', 'warning')
        return response
    
    
    session_record.last_activity = now
    db.session.commit()
    
    
    return None