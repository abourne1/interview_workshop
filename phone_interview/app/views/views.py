import logging
import random
import urllib2
from flask import Flask, render_template, redirect, url_for, request, flash
from app.models import Topic, Question, Recording
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


@app.route('/choose_question', methods=['GET', 'POST'])
def choose_question():
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
    action_url = "https://74d005c5.ngrok.io/call_again.xml?question={}".format(question.id)
    client.calls.create(
        to=phone_number,
        from_=app.config['TWILIO_NUMBER_1'],
        url=action_url
    )
    return render_template(
        'homepage.html',
        topics=db.session.query(Topic).all(),
        is_current=True
    )

@app.route('/handle_call', methods=['GET', 'POST'])
def handle_call():
    dial_call_sid = request.args.get('DialCallSid', '')
    rec = db.session.query(Recording).filter(Recording.call_sid == dial_call_sid).first()
    question = db.session.query(Question).get(rec.question_id)
    resp = twilio.twiml.Response()


@app.route('/repeat', methods=['GET', 'POST'])
def repeat():
    pass

@app.route('/hint', methods=['GET', 'POST'])
def hint():
    pass

@app.route('/answer', methods=['GET', 'POST'])
def answer():
    pass






