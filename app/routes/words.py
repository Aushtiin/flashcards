from flask import Blueprint, jsonify, request
from ..models import Word
from ..db import db

words_bp = Blueprint('words', __name__)

@words_bp.route('/api/words', methods=['GET'])
def get_words():
  words = Word.query.all()
  return jsonify([{
    'id': word.id,
    'word': word.word,
    'meaning': word.meaning,
    'tag': word.tag,
    'user_id': word.user_id
  } for word in words])

@words_bp.route('/api/words', methods=['POST'])
def add_word():
  data = request.get_json()

  if not data or not all(key in data for key in ('word', 'meaning', 'tag', 'user_id')):
    return jsonify({'message': 'Bad Request'}), 400
  
  word = data['word']
  meaning = data['meaning']
  tag = data['tag']
  user_id = data['user_id']
  
  new_word = Word(word=word, meaning=meaning, tag=tag, user_id=user_id)

  try: 
    db.session.add(new_word)
    db.session.commit()
    return jsonify({'message': 'Word added successfully'}), 201
  except Exception as e:
    db.session.rollback()
    return jsonify({'message': 'Internal Server Error', 'error': str(e)}), 500