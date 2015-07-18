import datetime
from app import db

class Question(db.Model):
    __tablename__ = 'questions'

    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(64))
    topic_id = db.Column(db.Integer, db.ForeignKey('topics.id'))
    text = db.Column(db.Text(2000))
    hint = db.Column(db.Text(2000))
    timestamp = db.Column(db.DateTime)
    popularity = db.Column(db.Integer)
    answer = db.Column(db.Text(2000))

    def __init__(self, text, hint, topic_id, answer):
        self.topic_id = topic_id
        self.text = text
        self.hint = hint
        self.timestamp = datetime.datetime.now()
        self.answer = answer
        self.popularity = 0

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

class Recording(db.Model):
    __tablename__ = 'recordings'

    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(200))
    call_sid = db.Column(db.String(300))
    sent = db.Column(db.Boolean)
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id'))

    def __init__(self, call_sid, question_id):
        self.call_sid = call_sid
        self.question_id = question_id


    def __repr__(self):
        return '<id {}>'.format(self.id)

