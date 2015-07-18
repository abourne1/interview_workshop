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
    return render_template(
        'new.html',
        topics=db.session.query(Topic).all()
    )

@app.route('/make', methods=['POST'])
def make():
    # add validations, probably through a form class
    text=request.form['question']
    hint=request.form['hint']
    topic_id=request.form['topic_id']
    answer=request.form['answer']
    new_question = Question(
        text=text,
        hint=hint,
        topic_id=topic_id,
        answer=answer
    )
    db.session.add(new_question)
    db.session.commit()
    flash('Question created')
    # msg = Message(
    #     "New Question",
    #     sender="from@example.com",
    #     recipients=[app.config['EMAIL_ADDR']]
    # )
    #msg.body("A new question has been submitted:\n" + text + "\n" + hint)
    #mail.send(msg)
    print 34
    return render_template(
        'homepage.html',
        topics=db.session.query(Topic).all(),
        questions=db.session.query(Question).all()
    )
# from recordings import 
