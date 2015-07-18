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

@app.route('/handle_recording', methods=["GET","POST"])
def handle_recording():
    new_recording = Recording(
        url=request.form['RecordingUrl'],
        call_sid=request.form['CallSid'],
        recording_sid=request.form['RecordingSid']
    )
    db.session.add(new_recording)
    db.session.commit()
    return "recording done"