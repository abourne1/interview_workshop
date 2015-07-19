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


@app.route('/new', methods=['GET', 'POST'])
def new():
    filename = "../interview_workshop/phone_interview/recordings/" + "recording-" + str(db.session.query(Recording).count() + 1) + ".wav"
    return render_template(
        'new.html',
        topics=db.session.query(Topic).all(),
        filename = filename,
        languages=[
            "python",
            "java",
            "javascript",
            "c"
        ]
    )

@app.route('/make', methods=['POST'])
def make():
    # add validations, probably through a form class
    text=request.form['question']
    hint=request.form['hint']
    topic_id=request.form['topic_id']
    answer=request.form['answer']
    language=request.form['language']
    new_question = Question(
        text=text,
        hint=hint,
        topic_id=topic_id,
        answer=answer,
        language=language
    )
    db.session.add(new_question)
    db.session.commit()
    flash('Question created')

    return render_template(
        'homepage.html',
        topics=db.session.query(Topic).all(),
        questions=db.session.query(Question).all()
    )

