import pandas as pd
import numpy as np
import time
import redis
import asyncio

from poloniex import PoloniexHttpAPI
from utils import validate_period_format
from candlesticks import parse_candles, resample_candles

class CandlesCacheService():

	def __init__(self, code, period, window, redis_conn, logger):
		validate_period_format(period)
		self.code = code
		self.period = period
		self.window = window
		self.redis_conn = redis_conn
		self.timestamp_key = f"{self.code.lower()}-timestamps:{self.period}"
		self.close_key = f"{self.code.lower()}-closes:{self.period}"
		self.logger = logger

	def timestamp_for_current_candle(self, optimum_period):
		return int(time.time() / optimum_period) * optimum_period

	def timestamp_for_previous_candle(self, optimum_period):
		return int(int(time.time() - optimum_period) / optimum_period) * optimum_period

	def retrieve(self):
		polo = PoloniexHttpAPI(offset=10)
		optimum_period, start, end = polo.get_chart_data_params(self.period, self.window)

		first_timestamp = self.redis_conn.zrange(self.timestamp_key, 0, 0)
		last_timestamp = self.redis_conn.zrange(self.timestamp_key, -1, -1)
		first_timestamp = first_timestamp[0] if bool(first_timestamp) else first_timestamp
		last_timestamp = last_timestamp[0] if bool(last_timestamp) else last_timestamp
		dicts = None
		if not(bool(first_timestamp)) or float(first_timestamp) > start or float(last_timestamp) < self.timestamp_for_previous_candle(optimum_period):
			self.logger.info('last candle: {}, previous candle: {}'.format( last_timestamp, self.timestamp_for_previous_candle(optimum_period)))
			dicts = self.send_request(polo, optimum_period, start, end)
			self.store(dicts)
		else:
			self.logger.info('No candles update required.')
		timestamps = self.redis_conn.zrange(self.timestamp_key, -1 if self.window ==1 else -(self.window-1) , -1)
		closes = self.redis_conn.hmget(self.close_key, timestamps)
		current_price = self.ticker()
		current_timestamp = self.timestamp_for_current_candle(optimum_period)
		timestamps.append(current_timestamp)
		closes.append(current_price)

		result = [{'date': t, 'close': c} for t, c in zip(timestamps, closes)]
		return result;

	def send_request(self, polo: PoloniexHttpAPI, period, start, end):
		# request to poloniex api
		req = polo.chart_data(self.code.upper(), period, start, end)
		loop = asyncio.new_event_loop()
		content = loop.run_until_complete(req)
		loop.close()

		# resample candles to period
		df = parse_candles(content)
		resampled = resample_candles(df, self.period)
		resampled.drop(resampled.index[-1])
		resampled['date'] = resampled['date'].map(lambda v : v.timestamp())
		return resampled[['date', 'close']].to_dict('records')

	def store(self, dicts):
		self.logger.info('Updating candles.')
		timestamps = {d['date']:d['date'] for d in dicts}
		prices = {d['date']: d['close'] for d in dicts}
		pipe = self.redis_conn.pipeline()
		pipe.zadd(self.timestamp_key, timestamps).hmset(self.close_key, prices)
		pipe.execute()

	def ticker(self):
		polo = PoloniexHttpAPI()
		req = polo.ticker()
		loop = asyncio.new_event_loop()
		content = loop.run_until_complete(req)
		loop.close()
		df = pd.read_json(content, orient='index')
		row = df.loc[self.code.upper()]
		return row['last']


