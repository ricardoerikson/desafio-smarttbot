from flask import Flask, render_template, redirect, url_for, request, json, session
from flask_wtf.csrf import CSRFProtect
from flask_bootstrap import Bootstrap
from flask_migrate import Migrate

import os
import time
import requests
import pandas as pd

from core.model import db

from expert_advisor import ExpertAdvisor
from currency_pairs_model import CurrencyPair
from bots_model import Bot
from trades_model import Trade

from bots_form import BotsForm

from apscheduler.schedulers.background import BackgroundScheduler

app = Flask(__name__)

app.config['SECRET_KEY'] = 'the-quick-brown-fox-jumps-over-the-lazy-dog'
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['RDBMS_URL']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

bootstrap = Bootstrap(app)
csrf = CSRFProtect(app)

db.init_app(app)
app.app_context().push()
Migrate(app, db)

sched = BackgroundScheduler()

@sched.scheduled_job('interval', seconds=3)
def evaluate_strategies():
	with app.app_context():
		bots = Bot.query.filter_by(active=1).all()
		app.logger.info('{} running bots'.format(len(bots)))
		for bot in bots:
			ea = ExpertAdvisor(bot, app, db)
			ea.evaluate_strategy()


sched.start()

@app.route('/eas')
def ea():
	bot = Bot.query.get(4)
	id = bot.opened_position()
	return str(id.id)

@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
def index():
	url = 'http://chart_data:5000/ticker'
	res = requests.get(url)
	df = pd.read_json(res.content, orient='index')
	df = df.reindex(columns=['last', 'percentChange', 'high24hr', 'low24hr', 'baseVolume'])
	df['font_color'] = df['percentChange'].map(lambda v: 'text-secondary' if v == 0 else ('text-success' if v > 0 else 'text-danger'))
	df.sort_index(ascending=True, inplace=True)
	return render_template('index.html', df=df)

@app.route('/bots', methods=['GET'])
def bots():
	bots = Bot.query.all()
	return render_template('bots.html', bots=bots)

@app.route('/bots/add', methods=['GET', 'POST'])
def bots_add():
	form = BotsForm()
	currencies = CurrencyPair.query.all()
	form.currency_pair_id.choices = [(pair.id, pair.code) for pair in currencies ]
	if form.validate_on_submit():
		bot = Bot()
		form.populate_obj(bot)
		bot.id = None
		db.session.add(bot)
		db.session.commit()
		return redirect(url_for('bots'))
	return render_template('bots_add.html', form = form)

@app.route('/bots/<int:id>/report', methods=['GET'])
def bots_report(id):
	bot = Bot.query.get(id)
	trades = bot.trades
	ea = ExpertAdvisor(bot, app, db)
	ea.update_data()
	return render_template('bots_report.html', bot = bot, trades=trades, current_price=ea.current_price)

@app.route('/bots/<int:id>/edit', methods=["GET", "POST"])
def bots_edit(id):
	bot = Bot.query.get_or_404(id, description='Bot não encontrado')
	form = BotsForm()
	currencies = [(pair.id, pair.code) for pair in CurrencyPair.query.all() ]
	if request.method == 'GET':
		form = BotsForm(obj=bot)
		form.currency_pair_id.choices = currencies
		form.currency_pair_id.default = bot.currency_pair_id
	if request.method == 'POST':
		form.currency_pair_id.choices = currencies
		if form.validate_on_submit():
			form.populate_obj(bot)
			if bot.active == 0:
				ea = ExpertAdvisor(bot, app, db)
				ea.close_position(update=True)
			db.session.commit()
			return redirect(url_for('bots'))
	return render_template('bots_edit.html', form=form)

if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0')