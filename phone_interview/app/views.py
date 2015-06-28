from flask import render_template, redirect, url_for
from .models import Topic, Question
from app import app
from app import db

@app.route('/index')
def index():
    return render_template(
        'index.html',
        topics=db.session.query(Topic).all()
    )

@app.route('/new', methods=['POST'])
def new(question, hint, author, difficulty, topic_id):
    new_question = Question(
        author=author,
        topic_id=topic_id,
        difficulty=difficulty,
        text=question,
        hint=hint
    )
    db.session.add(new_question)
    return redirect(url_for('index'))

