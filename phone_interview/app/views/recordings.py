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


@app.route('/handle_recording', methods=['POST'])
def handle_recording():
    recording_url = request.RecordingUrl
    call_sid = request.CallSid

    new_recording = Recording(
        url=recording_url,
        call_sid=call_sid
    )
    db.session.add(new_recording)
    db.session.commit()

def get_recording(call_sid):
    recordings = db.session.query(Recording).with_attributes(
        Recording.url
    ).filter(
        Recording.call_sid == call_sid,
        Recording.sent == False
    )
    audio_recording = None
    for r in recordings:
        # figure out how to combine these recordings when I fix the code that gets here
        r.sent = True
        req = urllib2.Request(r.url)

    db.session.commit()