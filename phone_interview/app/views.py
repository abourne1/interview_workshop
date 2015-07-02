import logging
import random
import urllib2
from flask import Flask, render_template, redirect, url_for, request, flash
from .models import Topic, Question, Recording
from flask.ext.mail import Message, Mail
from sqlalchemy import desc, func
from app import app, db, mail
from twilio.util import TwilioCapability
from twilio.rest import TwilioRestClient


"""
put a button on the website you can click, and recieve a phone call
https://www.twilio.com/docs/howto/walkthrough/click-to-call/php/laravel#0

Could make the home page one big phone button
"""

@app.route('/')
def homepage():
    application_sid = "AP6053400b8f663ea7ba9bbcbb41da1ae3"
    capability = TwilioCapability(app.config['ACCOUNT_SID'], app.config['AUTH_TOKEN'])
    capability.allow_client_outgoing(application_sid)
    token = capability.generate()

    return render_template(
        'homepage.html',
        topics=db.session.query(Topic).all(),
        token=token
    )

@app.route('/make_question')
def make_question():
    return render_template(
        'new.html',
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

@app.route('/choose_question', methods=['GET'])
def query():
    client = TwilioRestClient(app.config['ACCOUNT_SID'], app.config['AUTH_TOKEN'])
    num_questions = db.session.query(func.count(Question.id)).count()
    index = int(random.random()**2 * num_questions)
    topic_id = request.form['topic_id']
    if topic_id == 0:
        question = db.session.query(Question).order_by(Question.popularity).desc()[index]
    else:
        question = db.session.query(Question).filter(
            Question.topic_id == topic_id
        ).order_by(Question.popularity.desc())[index]

    # combine many recordings together somehow?
    app.logger.debug(question)
    action_url = "record.xml?question={}".format(question.id)
    client.calls.create(
        to=request.form['number'],
        from_=app.config['TWILIO_NUMBER'],
        url=action_url
    )
    return redirect(url_for('homepage'))


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








