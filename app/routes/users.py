from flask import Blueprint, jsonify, request, url_for
from flask_mail import Message
from ..models import User
from ..db import db
from ..utils.auth import generate_confirmation_token
from .. import mail
import jwt
import os

users_bp = Blueprint('users', __name__)

@users_bp.route('/api/users', methods=['GET'])
def get_users():
  users = User.query.all()
  return jsonify([{
    'id': user.id,
    'username': user.username,
    'email': user.email,
    'confirmed': user.confirmed
  } for user in users])

@users_bp.route('/api/users/register', methods=['POST'])
def register():
  try:
    data = request.get_json()
    email = data.get('email')
    username = data.get('username')

    if User.query.filter_by(email=email).first() is not None:
      return jsonify({'message': 'User already exists'}), 400
    
    new_user = User(email=email, username=username)
    db.session.add(new_user)
    db.session.commit()

    token = generate_confirmation_token(email)
    confirm_url = url_for('users.confirm_email', token=token, _external=True)
    html = f'<p>Please confirm your email by clicking on the following link: <a href="{confirm_url}">{confirm_url}</a></p>'
    send_email('Confirm Your Email Address', [email], html)

    return jsonify({'message': 'User registered. Please check your email to confirm your registration.'}), 201
  except Exception as e:
    db.session.rollback()
    return jsonify(error=str(e)), 500


@users_bp.route('/api/users/confirm/<token>', methods=['POST'])
def confirm_email(token):
  try:
    email = jwt.decode(token, os.getenv('SECRET_KEY'), algorithms=['HS256'])['sub']
  except jwt.ExpiredSignatureError:
    return jsonify({'message': 'The confirmation link has expired.'}), 400
  except jwt.InvalidTokenError:
    return jsonify({'message': 'Invalid confirmation link.'}), 400
  
  user = User.query.filter_by(email=email).first_or_404()
  if user.confirmed:
    return jsonify({'message': 'Account already confirmed.'}), 200

  user.confirmed = True
  db.session.add(user)
  db.session.commit()

  return jsonify({'message': 'You have confirmed your account. Thanks!'}), 200

def send_email(subject, recipients, html_body):
  msg = Message(subject, recipients=recipients, html=html_body)
  mail.send(msg)
