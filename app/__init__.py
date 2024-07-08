import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_mail import Mail
from dotenv import load_dotenv
from .db import db

load_dotenv() 

migrate = Migrate()
mail = Mail()

def create_app():
  app = Flask(__name__)
  app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
  app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
  app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER')
  app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT', 587))
  app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS', 'true').lower() in ['true', 'on', '1']
  app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
  app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
  app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_DEFAULT_SENDER')
  app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
  app.config['MAIL_SUPPRESS_SEND'] = True  

  db.init_app(app)
  migrate.init_app(app, db)
  mail.init_app(app)

  from .routes import users_bp, words_bp, phrases_bp

  app.register_blueprint(users_bp)
  app.register_blueprint(words_bp)
  app.register_blueprint(phrases_bp)

  return app
