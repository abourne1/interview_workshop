import datetime
from app import db
from sqlalchemy.dialects.postgresql import JSON

class Question(db.Model):
    __tablename__ = 'questions'

    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(64))
    topic_id = db.Column(db.Integer, db.ForeignKey('topics.id'))
    text = db.Column(JSON)
    hint = db.Column(JSON)
    difficulty = db.Column(db.Integer)
    timestamp = db.Column(db.DateTime)

    def __init__(self, text, hint, topic_id, author, difficulty):
        self.author = author
        self.topic_id = topic_id
        self.difficulty = difficulty
        self.text = text
        self.hint = hint
        self.timestamp = datetime.datetime.now()

    def __repr__(self):
        return '<id {}>'.format(self.id)

class Topic(db.Model):
    __tablename__ = 'topics'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<id {}>'.format(self.id)

