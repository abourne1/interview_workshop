import logging
import random
import urllib2
import twilio.twiml
from flask import Flask, render_template, redirect, url_for, request, flash
from app.models import Topic, Question, Recording
from flask.ext.mail import Message, Mail
from sqlalchemy import desc, func
from app import app, db, mail, logger, client
from twilio.util import TwilioCapability

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
    topic_id = request.args.get('topic_id', '')
    phone_number = request.args.get('number', '')
    if topic_id == "0":
        matches = db.session.query(Question).order_by(Question.popularity.desc())
        index = int(random.random()**2 * matches.count() )
        question = matches.all()[index]
    else:
        matches = db.session.query(Question).filter(
            Question.topic_id == topic_id
        ).order_by(Question.popularity.desc())
        index = int(random.random()**2 * matches.count() )
        question = matches.all()[index]

    # call my number, then have that number dial the users number
    url = "{}/handle_call?question_id={}&action=speak".format(app.config['NGROK_ROUTE'], question.id)
    call = client.calls.create(
        to=phone_number,
        from_=app.config['TWILIO_NUMBER_1'],
        url=url
    )

    return render_template(
        'homepage.html',
        topics=db.session.query(Topic).all(),
        is_current=True,
        call_sid=call.sid,
        question_id=question.id
    )

@app.route('/handle_call', methods=['GET', 'POST'])
def handle_call():
    action = request.args.get('action', '')
    question_id = request.args.get('question_id', '')
    logger.debug(question_id)
    question = db.session.query(Question).get(question_id)
    logger.debug("popularity")
    logger.debug(question.popularity)
    resp = twilio.twiml.Response()

    # record, say, and stay on the line. Allow the user to interact w/
    # the call using buttons on the webpage
    if action == "repeat":
        resp.say(question.text)
    elif action == "hint":
        resp.say(question.hint)
    else:
        resp.say(question.text)
        logger.debug(question.text)

    # pause for 5 min before hanging up
    resp.pause(length=60 * 5)
    return str(resp)

@app.route('/upvote', methods=['GET', 'POST'])
def upvote():
    question_id = request.args.get('question_id', '')
    sid = request.args.get('call_sid', '')

    question = db.session.query(Question).get(question_id)
    if question.popularity:
        question.popularity += 1
    else:
        question.popularity = 1
    db.session.commit()
    return render_template(
        'homepage.html',
        topics=db.session.query(Topic).all(),
        is_current=True,
        call_sid=sid,
        question_id=question_id
    )

@app.route('/repeat', methods=['GET', 'POST'])
def repeat():
    sid, question_id = get_sid_and_question_id()
    update_call(sid, question_id, "repeat")
    return render_template(
        'homepage.html',
        topics=db.session.query(Topic).all(),
        is_current=True,
        call_sid=sid,
        question_id=question_id
    )

@app.route('/hint', methods=['GET', 'POST'])
def hint():
    sid, question_id = get_sid_and_question_id()
    update_call(sid, question_id, "hint")
    return render_template(
        'homepage.html',
        topics=db.session.query(Topic).all(),
        is_current=True,
        call_sid=sid,
        question_id=question_id
    )

@app.route('/answer', methods=['GET', 'POST'])
def answer():
    sid, question_id = get_sid_and_question_id()
    update_call(sid, question_id, "answer")
    return render_template(
        'homepage.html',
        topics=db.session.query(Topic).all(),
        is_current=True,
        call_sid=sid,
        question_id=question_id
    )

def get_sid_and_question_id():
    sid = request.args.get('call_sid', '')
    question_id = request.args.get('question_id', '')
    return sid, question_id

def update_call(sid, question_id, action):
    url = "{}/handle_call?question_id={}&action={}".format(app.config['NGROK_ROUTE'], question_id, action)
    call = client.calls.update(sid, url=url, method="POST")


