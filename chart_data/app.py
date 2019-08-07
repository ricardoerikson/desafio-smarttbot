import os
import json
import asyncio
import time
import numpy as np
import pandas as pd

from flask import Flask, jsonify

from poloniex import PoloniexHttpAPI
from candles_cache import CandlesCacheService
from utils import convert_period_into_seconds, convert_period_into_pandas_freq

import redis

redis_conn = redis.Redis(os.environ['REDIS_URL'], decode_responses=True)

app = Flask(__name__)

@app.route('/candles/<string:currency_pair>/period/<string:period>/window/<int:window>')
def candles(currency_pair, period, window):
	cache = CandlesCacheService(currency_pair, period, window, redis_conn, app.logger)
	data = cache.retrieve()
	df = pd.DataFrame.from_dict(data)
	df['date'] = pd.to_datetime(df['date'].map(lambda v: int(float(v))), unit='s')
	df['close'] = df['close'].map(float)
	return app.response_class(response=df.to_json(orient='records'), status=200, mimetype='application/json')

@app.route('/ticker')
def ticker():
	polo = PoloniexHttpAPI()
	req = polo.ticker()
	loop = asyncio.new_event_loop()
	content = loop.run_until_complete(req)
	loop.close()
	df = pd.read_json(content, orient='index')
	return app.response_class(response=content, status=200, mimetype='application/json')


@app.route('/currencies')
def currencies():
	polo = PoloniexHttpAPI()
	req = polo.currencies()
	loop = asyncio.new_event_loop()
	content = loop.run_until_complete(req)
	loop.close()

	return app.response_class(response=content, status=200, mimetype='application/json')

if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0')
