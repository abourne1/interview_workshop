import logging
import random
import urllib2
import twilio.twiml
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
    return render_template(
        'homepage.html',
        topics=db.session.query(Topic).all()
    )

@app.route('/choose_question', methods=['GET', 'POST'])
def choose_question():
    logger.debug(request.args)
    client = TwilioRestClient(app.config['ACCOUNT_SID'], app.config['AUTH_TOKEN'])
    
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
    url = "{}/handle_call?question_id={}".format(app.config['NGROK_ROUTE'], question.id)
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
    logger.debug(request.args)
    action = request.args.get('action', '')
    question_id = request.args.get('question_id', '')
    call_sid = request.args.get('call_sid', '')
    logger.debug(question_id)
    question = db.session.query(Question).get(question_id)
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
    #return str(resp)
    return render_template(
        'homepage.html',
        topics=db.session.query(Topic).all(),
        is_current=True,
        call_sid=call_sid,
        question_id=question.id
    )

@app.route('/repeat', methods=['GET', 'POST'])
def repeat():
    send_action("repeat")

@app.route('/hint', methods=['GET', 'POST'])
def hint():
    sid = request.args.get('call_sid', '')
    question_id = request.args.get('question_id', '')
    url = "http://5f296970.ngrok.io/handle_call?question_id={}&action=repeat".format(question_id)
    call = client.calls.update(sid, url, "POST")

@app.route('/answer', methods=['GET', 'POST'])
def answer():
    pass

def send_action(action):
    client = TwilioRestClient(app.config['ACCOUNT_SID'], app.config['AUTH_TOKEN'])
    sid = request.args.get('call_sid', '')
    question_id = request.args.get('question_id', '')
    url = "{}/handle_call?question_id={}&action={}".format(app.config['NGROK_ROUTE'], question_id, action)
    # these args aren't coming in!!! 
    logger.debug(sid)
    logger.debug(url)
    call = client.calls.update(sid, url=url, method="POST")
    return render_template(
        'homepage.html',
        topics=db.session.query(Topic).all(),
        is_current=True,
        call_sid=call.sid,
        question_id=question_id
    )






