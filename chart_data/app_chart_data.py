import asyncio
import time
import numpy as np

from flask import Flask

from poloniex import PoloniexHttpAPI
from candlesticks import parse_candles, resample_candles
from utils import convert_period_into_seconds, convert_period_into_pandas_freq

app = Flask(__name__)

@app.route('/candles/<string:currency_pair>/period/<string:period>/window/<int:window>')
def candles(currency_pair, period, window):
	# request to poloniex api
	polo = PoloniexHttpAPI(offset=10)
	req = polo.chart_data(currency_pair.upper(), period, window)
	loop = asyncio.new_event_loop()
	content = loop.run_until_complete(req)
	loop.close()

	# resample candles to period
	df = parse_candles(content)
	resampled = resample_candles(df, period, window)
	return app.response_class(response=resampled.to_json(orient='records', date_format='epoch'), status=200, mimetype='application/json')

@app.route('/ticker')
def ticker():
	polo = PoloniexHttpAPI()
	req = polo.ticker()
	loop = asyncio.new_event_loop()
	content = loop.run_until_complete(req)
	loop.close()

	return app.response_class(response=content, status=200, mimetype='application/json')

@app.route('/currencies')
def currencies():
	polo = PoloniexHttpAPI()
	req = polo.ticker()
	loop = asyncio.new_event_loop()
	content = loop.run_until_complete(req)
	loop.close()

	return app.response_class(response=content, status=200, mimetype='application/json')

if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0')
