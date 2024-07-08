import json
from app import create_app
from app.models import Word, Phrase
from app.db import db

app = create_app()

with app.app_context():
  db.create_all()

  # List of JSON files to load
  json_files = ['words.json', 'phrases.json']

  for json_file in json_files:
    with open(json_file) as f:
      data = json.load(f)

    for item in data:
      # Determine if the item is a word or a phrase
      if 'word' in item:
        word = Word.query.filter_by(word=item['word']).first()
        if word is None:
          new_word = Word(word=item['word'], meaning=item['meaning'], tag=item['tag'])
          db.session.add(new_word)
      elif 'phrase' in item:
        phrase = Phrase.query.filter_by(phrase=item['phrase']).first()
        if phrase is None:
          new_phrase = Phrase(phrase=item['phrase'], meaning=item['meaning'], tag=item['tag'])
          db.session.add(new_phrase)

  db.session.commit()
  print("Database seeded!")
