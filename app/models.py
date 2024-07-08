from .db import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    confirmed = db.Column(db.Boolean, default=False)
    words = db.relationship('Word', backref='owner', lazy=True)
    phrases = db.relationship('Phrase', backref='owner', lazy=True)

    def __repr__(self):
        return f'<User {self.username}>'

class Word(db.Model):
    __tablename__ = 'word'
    
    id = db.Column(db.Integer, primary_key=True)
    word = db.Column(db.String(80), unique=True, nullable=False)
    meaning = db.Column(db.String(200), nullable=False)
    tag = db.Column(db.String(20), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)

    def __repr__(self):
        return f'<Word {self.word}>'

class Phrase(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    phrase = db.Column(db.String(500), unique=True, nullable=False)
    meaning = db.Column(db.String(500), nullable=False)
    tag = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)

    def __repr__(self):
        return f'<Phrase {self.phrase}>'
