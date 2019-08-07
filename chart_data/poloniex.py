import asyncio
import time
import numpy as np

from aiohttp import ClientSession
from utils import convert_period_into_seconds, validate_period_format

class PoloniexHttpAPI():
	"""
	Wrapper class to perform HTTP requests to Poloniex's public http API
	"""
	VALID_PERIODS = np.array([300, 900, 1800, 7200, 14400, 86400])

	def __init__(self, offset=10):
		self.uri = 'https://poloniex.com/public'
		self.offset = offset

	def optimum_period(intended_period):
		mod = intended_period % PoloniexHttpAPI.VALID_PERIODS
		index = np.argwhere(mod == 0).max()
		return PoloniexHttpAPI.VALID_PERIODS[index]

	async def fetch(self, method, command, params={}):
		"""
		Base method for http requests to public API

		Args:
		    method (str): http method
		    command (str): command parameter from poloniex api
		    params (dict, optional): request parameters

		Returns:
		    json: request result
		"""
		com = {'command': command}
		async with ClientSession() as session:
			async with session.request(method, self.uri, params={**com, **params}) as response:
				return await response.text()

	def get_chart_data_params(self, period, window):
		window_end = int(time.time())
		seconds = convert_period_into_seconds(period)
		optimum_period = int(PoloniexHttpAPI.optimum_period(seconds))
		window_start = int(np.ceil((window_end - seconds * (window+self.offset)) / optimum_period) * optimum_period)
		return optimum_period, window_start, window_end

	def chart_data(self, currencyPair, period, start, end):
		"""
		Returns candlestick chart data according to the given parameters

		Args:
		    currencyPair (str): currency pair. ex: BTC_XMR
		    period (int): period in seconds
		    start (int): initial time in unix epoch
		    end (int): end time in unix epoch

		Returns:
		    json: candlestick data
		"""
		params = {'currencyPair': currencyPair, 'period': period, 'start': start, 'end': end}
		return self.fetch('get', 'returnChartData', params)


	def ticker(self):
		"""
		Retrieves summary information for each currency pair listed on the exchange

		Returns:
		    json: currency data
		"""
		return self.fetch('get', 'returnTicker')


	def currencies(self):
		"""
		Returns the currency pairs

		Returns:
		    json: Information about the currency pairs
		"""
		return self.fetch('get', 'returnCurrencies')

