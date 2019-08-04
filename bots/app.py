from main import app

from flask import redirect, url_for
from main.core.models import db

from apscheduler.schedulers.background import BackgroundScheduler

# sched = BackgroundScheduler()

# @sched.scheduled_job('interval', seconds=3)
# def evaluate_strategies():
# 	bots = Bot.query.filter_by(active=1).all()
# 	app.logger.info('{} running bots'.format(len(bots)))
# 	for bot in bots:
# 		ea = ExpertAdvisor(bot, app, db)
# 		ea.evaluate_strategy()

# sched.start()

if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0')