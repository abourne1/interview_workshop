import logging
import random
import urllib2
from flask import Flask, render_template, redirect, url_for, request, flash
from .models import Topic, Question, Recording
from flask.ext.mail import Message, Mail
from sqlalchemy import desc, func
from app import app, db, mail, logger
from twilio.util import TwilioCapability
from twilio.rest import TwilioRestClient


"""
put a button on the website you can click, and recieve a phone call
https://www.twilio.com/docs/howto/walkthrough/click-to-call/php/laravel#0

Could make the home page one big phone button
"""

"""
Here's an idea: intermediary twilio phone number. Press call, which calls a twilio number that is configured to
1) record 2) dial a second number 3) end record. All repeat or hint commands go to the second twilio number, which
performs those actions.
"""

@app.route('/')
def homepage():
    application_sid = "AP6053400b8f663ea7ba9bbcbb41da1ae3"
    capability = TwilioCapability(app.config['ACCOUNT_SID'], app.config['AUTH_TOKEN'])
    capability.allow_client_outgoing(application_sid)

    return render_template(
        'homepage.html',
        topics=db.session.query(Topic).all(),
        is_current=False
    )

@app.route('/new', methods=['GET', 'POST'])
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

@app.route('/make', methods=['POST','GET'])
def new():
    # add validations, probably through a form class
    text=request.form['question']
    hint=request.form['hint']
    topic_id=request.form['topic_id']
    author=request.form['author']
    answer=request.form['answer']
    new_question = Question(
        text=text,
        hint=hint,
        topic_id=topic_id,
        author=author,
        answer=answer
    )
    db.session.add(new_question)
    db.session.commit()
    flash('Question added to database!')
    # msg = Message(
    #     "New Question",
    #     sender="from@example.com",
    #     recipients=[app.config['EMAIL_ADDR']]
    # )
    #msg.body("A new question has been submitted:\n" + text + "\n" + hint)
    #mail.send(msg)
    return render_template(
        'homepage.html',
        topics=db.session.query(Topic).all(),
        questions=db.session.query(Question).all()
    )

@app.route('/choose_question', methods=['GET', 'POST'])
def query():
    client = TwilioRestClient(app.config['ACCOUNT_SID'], app.config['AUTH_TOKEN'])
    num_questions = db.session.query(Question).count()
    logger.debug(num_questions)
    index = int(random.random()**2 * num_questions)
    logger.debug(index)
    topic_id = request.args.get('topic_id', '')
    phone_number = request.args.get('number', '')
    if topic_id == "0":
        question = db.session.query(Question).order_by(Question.popularity.desc()).all()[index]
    else:
        question = db.session.query(Question).filter(
            Question.topic_id == topic_id
        ).order_by(Question.popularity.desc()).all()[index]

    # combine many recordings together somehow?
    app.logger.debug(question)
    #action_url = "https://74d005c5.ngrok.io/record.xml?question={}".format(question.id)
    # client.calls.create(
    #     to=phone_number,
    #     from_=app.config['TWILIO_NUMBER_1'],
    #     url=action_url
    # )
    return render_template(
        'homepage.html',
        topics=db.session.query(Topic).all(),
        is_current=True
    )

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








