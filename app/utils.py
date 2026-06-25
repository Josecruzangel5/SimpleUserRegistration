import bcrypt 
import re 

def hash_password(plain_password):
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(plain_password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

def check_password(plain_password, hashed_password):
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

def is_valid_password(password):
    if len(password)<8:
        return False, "password must be at least 8 characters long"
    if not any(c.isdigit() for c in password):
        return False, "password must contain at least one number"
    if not any(c.isalpha() for c in password):
        return False, "password must contain at least a letter"
    return True, ""

def is_valid_name(name):
    name = name.strip()
    if len(name) < 5:
        return False, "full name must have at least 5 characters"
    return True, ""
