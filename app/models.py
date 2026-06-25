from app import db
from datetime import datetime
import uuid

class User(db.Model):
    __tablename__ = 'users'

id = db.Column(db.Integer, primary_key=True)
email = db.Column(db.String(254), unique=True, nullable=False, index=True)
full_name = db.Column(db.String(100), nullable=false)
password_hash = db.Column(db.String(128), nullable=false)
failed_attempts = db.Column(db.integer, default=0)
locked until = db.Column(db.DateTime, nullable=true)


session = db.relationship('Session', backref='user', uselist=False, cascade='all, delete-orphan')

def __repr__(self):
    return f'<User {self.email}>'

class Session(db.Model):
    __tablename__ = 'sessions'

id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True, nullable=False)
created_at = db.Column(db.DateTime, default=datetime.utcnow)
last_activity = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

def __repr__(self):
    return f'<Session {self.id} for user {self.user_id}>'