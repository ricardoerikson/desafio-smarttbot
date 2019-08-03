import os

from flask import Flask, render_template, redirect, url_for, request, json, session
from flask_wtf.csrf import CSRFProtect
from flask_bootstrap import Bootstrap
from flask_migrate import Migrate

app = Flask(__name__)

app.config['SECRET_KEY'] = 'the-quick-brown-fox-jumps-over-the-lazy-dog'
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['RDBMS_URL']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

bootstrap = Bootstrap(app)
csrf = CSRFProtect(app)

db.init_app(app)
app.app_context().push()
Migrate(app, db)

