import jwt
import os
import bcrypt
from datetime import datetime, timedelta

def create_employee_access_token(user_id):
     return jwt.encode({'user': str(user_id), 'type': 'access_token',
                        'exp': datetime.utcnow() + timedelta(minutes=15)}, 
                        os.environ.get("JWT_SECRET", "secret"), algorithm='HS256')

def validate_employee_access_token(jwt_encoded):
    try:
        jwt_encoded = jwt_encoded[7:] # Removing Bearer from Authorization header
        decoded = jwt.decode(jwt_encoded, os.environ.get("JWT_SECRET", "secret"), algorithms='HS256')
        if(decoded['type'] != 'access_token'):
            return False
        return True
    except Exception as e:
        print(e)
    return False
    
def create_employee_refresh_token(user):
     return jwt.encode({'user': user, 'type': 'refresh_token', 'exp': datetime.utcnow()+ timedelta(hours=24*7)}, 
            os.environ.get("JWT_SECRET", "secret"), algorithm='HS256')    

def validate_employee_refresh_token(jwt_encoded):
    try:
        decoded = jwt.decode(jwt_encoded, os.environ.get("JWT_SECRET", "secret"), algorithms='HS256')
        if(decoded['type'] != 'refresh_token'):
            return False, ''
        return True, str(decoded['user'])
    except Exception as e:
        print(e)
    return False, ''

def check_password(passwd, user_salt, passwd_hash):
    return bcrypt.hashpw(passwd.encode(), user_salt.encode()).decode('ascii') == passwd_hash

def generate_salt():
    return bcrypt.gensalt().decode('ascii')

def generate_password_hash(passwd, salt):
    p_hash = bcrypt.hashpw(passwd.encode(), salt.encode())
    p_hash = p_hash.decode('ascii')
    return p_hash