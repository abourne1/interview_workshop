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

@app.route('/next-question', methods=['GET', 'POST'])
def next_question():
    sid = request.args.get('call_sid', '')
    topic_id = request.args.get('topic_id', '')
    question = choose_question(topic_id)
    update_call(sid, question.id)
    return render_template(
        'in_call.html',
        topics=db.session.query(Topic).all(),
        is_current=True,
        call_sid=sid,
        question_id=question.id
    )

@app.route('/upvote', methods=['GET', 'POST'])
def upvote():
    sid, question_id, voted = get_params()

    question = db.session.query(Question).get(question_id)
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
        voted=True
    )

@app.route('/repeat', methods=['GET', 'POST'])
def repeat():
    sid, question_id, voted = get_params()
    update_call(sid, question_id, "repeat")
    return render_template(
        'in_call.html',
        topics=db.session.query(Topic).all(),
        is_current=True,
        call_sid=sid,
        question_id=question_id,
        voted=voted
    )

@app.route('/hint', methods=['GET', 'POST'])
def hint():
    sid, question_id, voted = get_params()

    update_call(sid, question_id, "hint")
    return render_template(
        'in_call.html',
        topics=db.session.query(Topic).all(),
        is_current=True,
        call_sid=sid,
        question_id=question_id,
        voted=voted
    )

@app.route('/answer', methods=['GET', 'POST'])
def answer():
    sid, question_id, voted = get_params()

    update_call(sid, question_id, "answer")
    return render_template(
        'in_call.html',
        topics=db.session.query(Topic).all(),
        is_current=True,
        call_sid=sid,
        question_id=question_id,
        voted=voted
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

def get_params():
    sid = request.args.get('call_sid', '')
    question_id = request.args.get('question_id', '')
    voted = request.args.get('voted', '')
    return sid, question_id, voted

def update_call(sid, question_id, action=""):
    url = "{}/handle_call?question_id={}&action={}".format(app.config['NGROK_ROUTE'], question_id, action)
    call = client.calls.update(sid, url=url, method="POST")