import pandas as pd
import requests

from app.bots.models import Bot, Trade

class ExpertAdvisor():

	def __init__(self, bot, app, db):
		self.bot = bot
		self.current_price = 0
		self.db = db
		self.app = app

	def request_data(self):
		code = self.bot.currency_pair.code
		period = self.bot.period
		num_candles = max(self.bot.short_sma, self.bot.long_sma)

		url = f"http://chart_data:5000/candles/{code.lower()}/period/{period}/window/{num_candles}"
		response = requests.get(url)
		return response.content

	def buy(self):
		self.app.logger.info('Buy trade for #{} - {}'.format(self.bot.id, self.bot.name))
		self.open_trade('B')

	def sell(self):
		self.app.logger.info('Sell trade for #{} - {}'.format(self.bot.id, self.bot.name))
		self.open_trade('S')

	def open_trade(self, trade_type):
		trade = Trade()
		trade.enter_price = self.current_price
		trade.amount = self.bot.amount
		trade.trade_type = trade_type
		trade.currency_pair_id = self.bot.currency_pair_id
		trade.bot_id = self.bot.id
		self.db.session.add(trade)
		self.db.session.commit()

	def update_data(self):
		data = self.request_data()
		self.df = pd.read_json(data, orient='records')
		self.current_price = float(self.df.iloc[-1]['close'])


	def evaluate_strategy(self):
		self.update_data()
		if self.needs_close():
			self.close_position()

		self.df['short_sma'] = self.df['close'].rolling(int(self.bot.short_sma)).mean()
		self.df['long_sma'] = self.df['close'].rolling(int(self.bot.long_sma)).mean()
		self.df['position'] = self.df['short_sma'] > self.df['long_sma']
		self.df['position'] = self.df['position'] - self.df['position'].shift(1)
		last_candle = self.df.iloc[-1]
		if self.bot.position() is None:
			if last_candle['position'] == 1:
				self.buy()
			if last_candle['position'] == -1:
				self.sell()

		self.app.logger.info('Nothing to do for #{} - {}'.format(self.bot.id, self.bot.name))

	def close_position(self, update=False):
		if update == True:
			self.update_data()
		position = self.bot.position()
		if position is None:
			return
		position.exit_price = self.current_price
		self.db.session.commit()
		self.app.logger.info('Closing position for #{} - {}'.format(self.bot.id, self.bot.name))

	def needs_close(self):
		position = self.bot.position()
		if position is None:
			return False
		if position.trade_type == 'B':
			if self.current_price >= position.enter_price + self.bot.gain_size  or self.current_price <= position.enter_price - self.bot.loss_size:
				return True
		if position.trade_type == 'S':
			if self.current_price <= position.enter_price - self.bot.gain_size  or self.current_price >= position.enter_price + self.bot.loss_size:
				return True
		return False

