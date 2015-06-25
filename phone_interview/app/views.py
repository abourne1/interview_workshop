from flask import render_template
from .models import Topic
from app import app

@app.route('/')
@app.route('/index')
def index():
    return render_template(
        'index.html',
        topics=Topic.all
    )
