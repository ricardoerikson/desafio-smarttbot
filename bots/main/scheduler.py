import main

from main.core.models import db
from main.bots.models import Bot
from main.expert_advisor import ExpertAdvisor

from apscheduler.schedulers.background import BackgroundScheduler

sched = BackgroundScheduler()

@sched.scheduled_job('interval', seconds=10, id='job')
def evaluate_strategies():
	with main.app.app_context():
		bots = Bot.query.filter_by(active=1).all()
		main.app.logger.info('{} running bots'.format(len(bots)))
		for bot in bots:
			ea = ExpertAdvisor(bot, main.app, db)
			ea.evaluate_strategy()
