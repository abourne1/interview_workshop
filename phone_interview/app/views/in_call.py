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

@app.route('/in_call', methods=["GET"])
def in_call():
    return render_template(
        'in_call.html'
    )

@app.route('/next-question', methods=['GET', 'POST'])
def next_question():
    sid = request.args.get('call_sid', '')
    topic_id = request.args.get('topic_id', '')
    question = pick_question(topic_id)
    update_call(sid, question.id)
    return render_template(
        'in_call.html',
        topics=db.session.query(Topic).all(),
        is_current=True,
        call_sid=sid,
        question_id=question.id,
        languages=app.config["LANGUAGES"],
        answer=question.answer,
        answer_language=question.language
    )

@app.route('/upvote', methods=['GET', 'POST'])
def upvote():
    sid, question_id, voted, user_input = get_params()
    question = db.session.query(Question).get(question_id)
    user_input = request.args.get('user_input', '')
    language = request.args.get('language', '')

    if question.popularity:
        question.popularity += 1
    else:
        question.popularity = 1
    db.session.commit()
    return render_template(
        'in_call.html',
        topics=db.session.query(Topic).all(),
        is_current=True,
        call_sid=sid,
        question_id=question_id,
        voted=True,
        languages=app.config["LANGUAGES"],
        user_input = user_input,
        language = language,
        answer=question.answer,
        answer_language=question.language
    )

@app.route('/repeat', methods=['GET', 'POST'])
def repeat():
    sid, question_id, voted, user_input = get_params()
    question = db.session.query(Question).get(question_id)
    update_call(sid, question_id, "repeat")
    return render_template(
        'in_call.html',
        topics=db.session.query(Topic).all(),
        is_current=True,
        call_sid=sid,
        question_id=question_id,
        voted=voted,
        languages=app.config["LANGUAGES"],
        answer=question.answer,
        language = request.args.get('language', ''),
        user_input = user_input,
        answer_language=question.language
    )

@app.route('/hint', methods=['GET', 'POST'])
def hint():
    sid, question_id, voted, user_input = get_params()
    question = db.session.query(Question).get(question_id)
    update_call(sid, question_id, "hint")
    return render_template(
        'in_call.html',
        topics=db.session.query(Topic).all(),
        is_current=True,
        call_sid=sid,
        question_id=question_id,
        voted=voted,
        languages=app.config["LANGUAGES"],
        answer=question.answer,
        language = request.args.get('language', ''),
        user_input = user_input,
        answer_language=question.language
    )

@app.route('/hangup', methods=['GET', 'POST'])
def hangup():
    sid = request.args.get('call_sid', '')
    call = client.calls.update(sid, status="completed")
    return render_template(
        'homepage.html',
        topics=db.session.query(Topic).all(),
        is_current=False
    )

def pick_question(topic_id):
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
    return question

def get_params():
    sid = request.args.get('call_sid', '')
    question_id = request.args.get('question_id', '')
    voted = request.args.get('voted', '')
    user_input = request.args.get('user_input', '')
    return sid, question_id, voted, user_input

def update_call(sid, question_id, action=""):
    url = "{}/handle_call?question_id={}&action={}".format(app.config['NGROK_ROUTE'], question_id, action)
    call = client.calls.update(sid, url=url, method="POST")