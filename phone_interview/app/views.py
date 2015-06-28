from flask import render_template, redirect, url_for, request, flash
from .models import Topic, Question
from app import app
from app import db

@app.route('/')
def index():
    return render_template(
        'index.html',
        topics=db.session.query(Topic).all(),
        questions=db.session.query(Question).all(),
        difficulties={
            1: "brogrammer",
            2: "application developer",
            3: "library writer",
            4: "language creator",
            5: "linus torvalds"
        }
    )

@app.route('/new', methods=['POST'])
def new():
    new_question = Question(
        author=request.form['author'],
        topic_id=request.form['topic_id'],
        difficulty=request.form['difficulty'],
        text=request.form['question'],
        hint=request.form['hint']
    )
    db.session.add(new_question)
    db.session.commit()
    flash('Question added to database!')
    return redirect(url_for('index'))

@app.route('/call', methods=['GET'])
def call():
    """
    make a phone menu, filter, speak, record, text recording
    :return:
    """
    pass
