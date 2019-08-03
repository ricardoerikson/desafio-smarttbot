
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

sched = BackgroundScheduler()

@sched.scheduled_job('interval', seconds=10)
def evaluate_strategies():
	with app.app_context():
		bots = Bot.query.filter_by(active=1).all()
		app.logger.info('{} running bots'.format(len(bots)))
		for bot in bots:
			ea = ExpertAdvisor(bot, app, db)
			ea.evaluate_strategy()


sched.start()

if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0')