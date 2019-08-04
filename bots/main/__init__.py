import os

from flask import Flask, render_template, redirect, url_for, request, json, session
from flask_wtf.csrf import CSRFProtect
from flask_bootstrap import Bootstrap
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from main.core.models import db

# import blueprints
from main.bots.routes import bots_blueprint
from main.home.routes import home_blueprint
from main.currencies.routes import currencies_blueprint


def create_app():
	app = Flask(__name__)

	app.config['SECRET_KEY'] = 'the-quick-brown-fox-jumps-over-the-lazy-dog'
	app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['RDBMS_URL']
	app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

	# Extensions configuration for Flask

	bootstrap = Bootstrap(app)
	csrf = CSRFProtect(app)
	Migrate(app, db)
	db.init_app(app)

	# Blueprints register
	app.register_blueprint(bots_blueprint, url_prefix='/bots')
	app.register_blueprint(currencies_blueprint, url_prefix='/currencies')
	app.register_blueprint(home_blueprint)
	return app

app = create_app()