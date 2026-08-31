import os
from datetime import datetime, timedelta, timezone
from functools import wraps
from flask import request, jsonify
from jose import jwt
import jose
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv('SECRET_KEY') or "a-super-secret-key-change-this"

def encode_token(customer_id):
    payload = {
        'exp': datetime.now(timezone.utc) + timedelta(hours=1),  # Token expires in 1 hour
        'iat': datetime.now(timezone.utc),  # Issued at time
        'sub': str(customer_id)  # Subject of the token (customer ID) - must be a string per JWT spec
    }
    
    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    return token

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split(" ")[1]  # Expecting 'Bearer <token>'
        
        if not token:
            return jsonify({'message': 'Token is missing!'}), 401

        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
            current_customer_id = payload['sub']
        except jose.exceptions.ExpiredSignatureError:
            return jsonify({'message': 'Token has expired!'}), 401
        except jose.exceptions.JWTError:
            return jsonify({'message': 'Invalid token!'}), 401

        return f(current_customer_id, *args, **kwargs)

    return decorated