import datetime
from app import db
from time import strftime

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
    language = db.Column(db.String(64))

    def __init__(self, text, hint, topic_id, answer, language):
        self.topic_id = topic_id
        self.text = text
        self.hint = hint
        self.timestamp = datetime.datetime.now()
        self.answer = answer
        self.popularity = 0
        self.language=language

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
    recording_sid = db.Column(db.String(300))
    sent = db.Column(db.Boolean)
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id'))
    timestamp = db.Column(db.DateTime)

    def __init__(self, url, call_sid, recording_sid):
        self.url = url
        self.call_sid = call_sid
        self.recording_sid = recording_sid
        self.timestamp = datetime.datetime.now()

    def question(self):
        if self.question_id:
            return db.session.query(Question).get(self.question_id)
        else: 
            return ""

    def prettify(self):
        return self.remove_zero(self.timestamp.strftime("%a, %d %b %Y %I:%M %p")) if self.timestamp else ""

    def remove_zero(self, timestamp):
        time_list = timestamp.split()
        if time_list[-2][0]=='0':
            time_list[-2] = time_list[-2][1:]
        return ' '.join(time_list)  

    def __repr__(self):
        return '<id {}>'.format(self.id)

