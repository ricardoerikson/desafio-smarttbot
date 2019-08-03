from flask import Blueprint, render_template, redirect, url_for

from app import db
from app.bots.models import Bot
from app.bots.forms import BotsForm

bots_blueprints = Blueprint('bots', __name__, templates_folder = 'templates')

@bots_blueprints.route('/', methods=['GET'])
def index():
	bots = Bot.query.all()
	return render_template('index.html', bots=bots)

@bots_blueprints.route('/add', methods=['GET', 'POST'])
def add():
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
	return render_template('add.html', form = form)

@bots_blueprints.route('/<int:id>/trades', methods=['GET'])
def trades(id):
	bot = Bot.query.get(id)
	trades = bot.trades
	ea = ExpertAdvisor(bot, app, db)
	ea.update_data()
	return render_template('trades.html', bot = bot, trades=trades, current_price=ea.current_price)

@bots_blueprints.route('/<int:id>/edit', methods=["GET", "POST"])
def edit(id):
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
			if bot.active == 0 or form.currency_pair_id != bot.currency_pair_id:
				ea = ExpertAdvisor(bot, app, db)
				ea.close_position(update=True)
			form.populate_obj(bot)
			db.session.commit()
			return redirect(url_for('bots'))
	return render_template('edit.html', form=form)

