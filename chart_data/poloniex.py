import asyncio
import numpy as np

from aiohttp import ClientSession

class PoloniexHttpAPI():
	"""
	Wrapper class to perform HTTP requests to Poloniex's public http API
	"""
	VALID_PERIODS = np.array([300, 900, 1800, 7200, 14400, 86400])

	def __init__(self):
		self.uri = 'https://poloniex.com/public'

	def optimum_period(intended_period):
		mod = intended_period % PoloniexHttpAPI.VALID_PERIODS
		index = np.argwhere(mod == 0).max()
		return PoloniexHttpAPI.VALID_PERIODS[index]

	def timestamp(self, date, format="%Y-%m-%d %H-%M"):
		"""
		Converts date in str format into unix timestamp

		Args:
		    date (str): date in str format
		    format (str, optional): format parameters

		Returns:
		    int: unix timestamp format
		"""
		return time.mktime(time.strptime(date, format))

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

	def chart_data(self, currencyPair, period, start, end):
		"""
		Returns candlestick chart data according to the given parameters

		Args:
		    currencyPair (str): currency pair. ex: BTC_XMR
		    period (int): period in seconds. valid values are 300, 900, 1800, 7200, 14400 and 86400
		    start (int): start of the window in seconds since the unix epoch
		    end (int): end of the window in seconds since the unix epoch

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

