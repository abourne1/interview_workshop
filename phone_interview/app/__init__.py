import sys

from flask import Flask

from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.mail import Mail

app = Flask(__name__)
app.config.from_pyfile("../config.py")
db = SQLAlchemy(app)
mail = Mail(app)
logger = app.logger

import logging

app.logger.addHandler(logging.StreamHandler(sys.stdout))
app.logger.setLevel(logging.DEBUG)

app.logger.debug("Hello World")
from app.views import views
