import os

from flask import Flask, render_template, redirect, url_for, request, json, session
from flask_wtf.csrf import CSRFProtect
from flask_bootstrap import Bootstrap
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from app.core.models import db
from app.bots.routes import bots_blueprint
from app.currencies.routes import currencies_blueprint

app = Flask(__name__)


app.config['SECRET_KEY'] = 'the-quick-brown-fox-jumps-over-the-lazy-dog'
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['RDBMS_URL']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Extensions configuration for Flask

bootstrap = Bootstrap(app)
csrf = CSRFProtect(app)
db = SQLAlchemy(app)
Migrate(app, db)
db.init_app(app)

# Blueprints register
app.register_blueprint(bots_blueprint, url_prefix='/bots')
app.register_blueprint(currencies_blueprint, url_prefix='/currencies')