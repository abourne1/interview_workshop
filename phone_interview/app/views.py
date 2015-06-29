from flask import render_template, redirect, url_for, request, flash
from .models import Topic, Question
from flaskext.mail import Message
from sqlalchemy import desc
from app import app, db, mail

"""
put a button on the website you can click, and recieve a phone call
https://www.twilio.com/docs/howto/walkthrough/click-to-call/php/laravel#0

Could make the home page one big phone button
"""

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
    # add validations, probably through a form class
    new_question = Question(
        author=request.form['author'],
        topic_id=request.form['topic_id'],
        text=request.form['question'],
        hint=request.form['hint'],
        answer=request.form['answer']
    )
    db.session.add(new_question)
    db.session.commit()
    flash('Question added to database!')
    msg = Message(
        "New Question",
        sender="from@example.com",
        recipients=[app.config['EMAIL_ADDR']]
    )
    msg.body("A new question has been submitted:\n" +
             request.form['question'] + "\n" +
             request.form['hint']
             )
    mail.send(msg)
    return redirect(url_for('index'))

@app.route('/choose_topic', methods=['POST'])
def choose_topic():
    resp = twilio.twiml.Response()
    with resp.gather(numDigits=1, action="/choose_question", method="POST") as g:
        g.say("Press 0 for any topic")
        for i, topic in enumerate( db.session.query(Topic).all() ):
            g.say("Press {} for {} questions".format(i, topic.name))

@app.route('/choose_question', methods=['POST'])
def query():
    digit_pressed = request.values.get('Digits', None)
    if digit_pressed == 0:
        question = db.session.query(Question).order_by(Question.popularity).desc()[0]
        # randomize later if necessary
    else:
        question = db.session.query(Question).filter(
            Question.topic_id).name == digit_pressed
        ).order_by(Question.popularity.desc())[0]
    # combine many recordings together somehow?
    render_template('record.xml', question = question)

@app.route('/control_question', methods=['POST'])
def control_quesition():
    digit_pressed = request.values.get('Digits', None)



