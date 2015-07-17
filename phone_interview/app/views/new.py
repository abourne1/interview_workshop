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


@app.route('/new', methods=['GET', 'POST'])
def make_question():
    return render_template(
        'new.html',
        topics=db.session.query(Topic).all()
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