from flask import Blueprint, jsonify, request
from ..models import Phrase
from ..db import db

phrases_bp = Blueprint('phrases', __name__)

@phrases_bp.route('/api/phrases', methods=['GET'])
def get_phrases():
    phrases = Phrase.query.all()
    return jsonify([{
    'id': phrase.id,
    'phrase': phrase.phrase,
    'meaning': phrase.meaning,
    'tag': phrase.tag,
    'user_id': phrase.user_id
    } for phrase in phrases])

@phrases_bp.route('/api/phrases', methods=['POST'])
def add_phrase():
  data = request.get_json()

  if not data or not all(key in data for key in ('phrase', 'meaning', 'tag', 'user_id')):
     return jsonify({'message': 'Bad Request'}), 400
  
  phrase = data['phrase']
  meaning = data['meaning']
  tag = data['tag']
  user_id = data['user_id']

  new_phrase = Phrase(phrase=phrase, meaning=meaning, tag=tag, user_id=user_id)

  try: 
    db.session.add(new_phrase)
    db.session.commit()
    return jsonify({'message': 'Phrase added successfully'}), 201
  except Exception as e:
    db.session.rollback()
    return jsonify({'message': 'Internal Server Error', 'error': str(e)}), 500