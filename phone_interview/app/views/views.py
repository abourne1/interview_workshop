import logging
import random
import urllib2
import twilio.twiml
import time
from flask import Flask, render_template, redirect, url_for, request, flash
from app.models import Topic, Question, Recording
from flask.ext.mail import Message, Mail
from sqlalchemy import desc, func
from app import app, db, mail, logger, client
from twilio.util import TwilioCapability
from new import new, make
from in_call import next_question, upvote, repeat, hint, pick_question
from recordings import handle_recording, recordings

"""
7/18/2015 Notes and betterments:

Make a user model, add login, store all recordings for a user. Add a media player to let users listen to their recordings

If really feeling like it, let user submit audio questions
"""

@app.route('/')
def homepage():
    return render_template(
        'homepage.html',
        topics=db.session.query(Topic).all(),
        is_current=False
    )


@app.route('/choose_question', methods=['GET', 'POST'])
def choose_question():
    topic_id = request.args.get('topic_id', '')
    phone_number = request.args.get('number', '')
    record = ("on" == request.args.get('if_record', ''))
    logger.debug(record)
    question = pick_question(topic_id)
    url = "{}/handle_call?question_id={}&action=speak".format(app.config['NGROK_ROUTE'], question.id)
    call = client.calls.create(
        to=phone_number,
        from_=app.config['TWILIO_NUMBER_1'],
        url=url,
        record=record,
        status_callback=app.config['NGROK_ROUTE'] + "/handle_recording",
        status_callback_method="POST"
    )

    return render_template(
        'in_call.html',
        topics=db.session.query(Topic).all(),
        is_current=True,
        call_sid=call.sid,
        question_id=question.id,
        languages=app.config["LANGUAGES"],
        answer=question.answer,
        answer_language=question.language
    )

@app.route('/handle_call', methods=['GET', 'POST'])
def handle_call():
    action = request.args.get('action', '')
    question_id = request.args.get('question_id', '')
    question = db.session.query(Question).get(question_id)
    resp = twilio.twiml.Response()

    if action == "repeat":
        resp.say(question.text)
    elif action == "hint":
        resp.say(question.hint)
    elif action == "answer":
        resp.say(question.answer)
    else:
        resp.say(question.text)
        logger.debug(question.text)

    # pause for 5 min before hanging up
    resp.pause(length=60 * 5)
    return str(resp)




