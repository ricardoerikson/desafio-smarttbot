import asyncio
from flask import Flask

from poloniex import PoloniexHttpAPI

app = Flask(__name__)

@app.route('/candles/<string:currency_pair>/period/<string:period>')
def candles(currency_pair):
	polo = PoloniexHttpAPI()
	req = polo.chart_data(currency_pair.upper(), 300, 1546300800, 1546646400)
	loop = asyncio.new_event_loop()
	content = loop.run_until_complete(req)
	loop.close()
	return app.response_class(response=content, status=200, mimetype='application/json')

if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0')
