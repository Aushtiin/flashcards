import jwt
import os
from datetime import datetime, timedelta

def generate_confirmation_token(email):
  payload = {
    'exp': datetime.utcnow() + timedelta(hours=24),
    'iat': datetime.utcnow(),
    'sub': email
  }

  return jwt.encode(payload, os.getenv('SECRET_KEY'), algorithm='HS256')