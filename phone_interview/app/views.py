from flask import render_template, redirect, url_for, request, flash
from .models import Topic, Question, Recording
from flaskext.mail import Message
from sqlalchemy import desc, func
from app import app, db, mail
import random
import twilio
import urllib2

"""
put a button on the website you can click, and recieve a phone call
https://www.twilio.com/docs/howto/walkthrough/click-to-call/php/laravel#0

Could make the home page one big phone button
"""

@app.route('/')
def homepage():
    render_template(
        'homepage',
        topics=db.session.query(Topic).all()
    )

@app.route('/make_question')
def make_question():
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
    num_questions = db.session.query(func.count(Question.id))
    index = int(random.random()**2 * num_questions)
    if digit_pressed == 0:
        question = db.session.query(Question).order_by(Question.popularity).desc()[index]
        # randomize later if necessary
    else:
        question = db.session.query(Question).filter(
            Question.topic_id == digit_pressed
        ).order_by(Question.popularity.desc())[index]

    # combine many recordings together somehow?
    action_url = "/control_question?question={}".format(question.id)
    render_template('record.xml', url=action_url)

@app.route('/control_question', methods=['POST'])
def control_quesition():
    question = db.session.query(Question).get(request.question)
    resp = twilio.twiml.Response()
    digit_pressed = request.values.get('Digits', None)
    call_sid = request.CallSid
    if digit_pressed == "1":
        resp.say(question.text)
    elif digit_pressed == "2":
        resp.say(question.hint)
    elif digit_pressed == "3":
        resp.say(question.answer)
    elif digit_pressed == "4":
        question.popularity += 1
        db.session.commit()
    elif digit_pressed == "5":
        r = get_recording(call_sid)
        # send recording to users email?
        client.calls.get(call_sid).hangup()

    action_url = "/control_question?question={}".format(question.id)
    render_template('record.xml', url=action_url)

@app.route('/handle_recording', methods=['POST'])
def handle_recording():
    recording_url = request.RecordingUrl
    call_sid = request.CallSid

    new_recording = Recording(
        url=recording_url,
        call_sid=call_sid
    )
    db.session.add(new_recording)
    db.session.commit()

def get_recording(call_sid):
    recordings = db.session.query(Recording).with_attributes(
        Recording.url
    ).filter(
        Recording.call_sid == call_sid,
        Recording.sent == False
    )
    audio_recording = None
    for r in recordings:
        # figure out how to combine these recordings when I fix the code that gets here
        r.sent = True
        req = urllib2.Request(r.url)

    db.session.commit()








