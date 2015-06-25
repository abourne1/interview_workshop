from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config.from_pyfile("../config.py")
db = SQLAlchemy(app)

from app import views, models

