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

@app.route('/recordings', methods=["GET","POST"])
def recordings():
    return render_template(
        'recordings.html',
        recordings=db.session.query(Recording).order_by(Recording.timestamp.desc()).all()
    )


@app.route('/handle_recording', methods=["GET","POST"])
def handle_recording():
    print "HERE!"
    print request.form
    new_recording = Recording(
        url=request.form['RecordingUrl'],
        call_sid=request.form['CallSid'],
        recording_sid=request.form['RecordingSid'],
    )
    db.session.add(new_recording)
    db.session.commit()
    return render_template(
        'homepage.html',
        topics=db.session.query(Topic).all(),
        is_current=False
    )
