import logging
import random
import urllib2
from flask import Flask, render_template, redirect, url_for, request, flash
from app.models import Topic, Question, Recording
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
    return render_template(
        'homepage.html',
        is_current=False,
        topics=db.session.query(Topic).all()
    )

@app.route('/call')
def make_call():
    logger.debug("first line")
    client = TwilioRestClient(app.config['ACCOUNT_SID'], app.config['AUTH_TOKEN'])

    topic_id = request.args.get('topic_id', '')
    phone_number = request.args.get('number', '')

    if topic_id == "0":
        num_questions = db.session.query(Question).count()
        index = int(random.random()**2 * num_questions)
        question = db.session.query(Question).order_by(Question.popularity.desc()).all()[index]
    else:
        matches = db.session.query(Question).filter(
            Question.topic_id == topic_id
        ).order_by(Question.popularity.desc())
        num_questions = matches.count()
        index = int(random.random()**2 * num_questions)
        question = matches.all()[index]

    # combine many recordings together somehow?
    action_url = "http://5f296970.ngrok.io/make_call.xml"
    call = client.calls.create(
        to=phone_number,
        from_=app.config['TWILIO_NUMBER_1'],
        url=action_url
    )
    logger.debug(2)
    logger.debug(call)
    logger.debug(3)
    return render_template(
        'homepage.html',
        is_current=False,
        topics=db.session.query(Topic).all()
    )


@app.route('/receive_call', methods=['GET', 'POST'])
def receive_call():
    pass

@app.route('/repeat', methods=['GET', 'POST'])
def repeat():
    pass

@app.route('/hint', methods=['GET', 'POST'])
def hint():
    pass

@app.route('/answer', methods=['GET', 'POST'])
def answer():
    pass






