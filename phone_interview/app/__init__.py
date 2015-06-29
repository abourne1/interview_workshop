import datetime
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flaskext.mail import Mail

app = Flask(__name__)
app.config.from_pyfile("../config.py")
db = SQLAlchemy(app)
mail = Mail(app)

from app import views
