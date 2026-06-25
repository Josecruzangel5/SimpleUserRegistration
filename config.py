import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET KEY')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

SESSION_TIMEOUT_MINUTES = 15
LOCKOUT_HOURS = 2
MAX_LOGIN_ATTEMPTS = 3