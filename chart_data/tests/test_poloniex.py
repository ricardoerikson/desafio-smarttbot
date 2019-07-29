import unittest2 as unittest

from poloniex import PoloniexHttpAPI
from utils import convert_period_into_seconds

class TestPoloniexAPI(unittest.TestCase):

	def test_optimum_period_for_5m(self):
		sec = convert_period_into_seconds('5m')
		optimum = PoloniexHttpAPI.optimum_period(sec)
		self.assertEqual(optimum, 300)

	def test_optimum_period_for_10m(self):
		sec = convert_period_into_seconds('10m')
		optimum = PoloniexHttpAPI.optimum_period(sec)
		self.assertEqual(optimum, 300)

	def test_optimum_period_for_20m(self):
		sec = convert_period_into_seconds('20m')
		optimum = PoloniexHttpAPI.optimum_period(sec)
		self.assertEqual(optimum, 300)

	def test_optimum_period_for_15m(self):
		sec = convert_period_into_seconds('15m')
		optimum = PoloniexHttpAPI.optimum_period(sec)
		self.assertEqual(optimum, 900)

	def test_optimum_period_for_45m(self):
		sec = convert_period_into_seconds('45m')
		optimum = PoloniexHttpAPI.optimum_period(sec)
		self.assertEqual(optimum, 900)

	def test_optimum_period_for_30m(self):
		sec = convert_period_into_seconds('30m')
		optimum = PoloniexHttpAPI.optimum_period(sec)
		self.assertEqual(optimum, 1800)

	def test_optimum_period_for_60m(self):
		sec = convert_period_into_seconds('60m')
		optimum = PoloniexHttpAPI.optimum_period(sec)
		self.assertEqual(optimum, 1800)

	def test_optimum_period_for_1h(self):
		sec = convert_period_into_seconds('1h')
		optimum = PoloniexHttpAPI.optimum_period(sec)
		self.assertEqual(optimum, 1800)

	def test_optimum_period_for_3h(self):
		sec = convert_period_into_seconds('3h')
		optimum = PoloniexHttpAPI.optimum_period(sec)
		self.assertEqual(optimum, 1800)

	def test_optimum_period_for_4h(self):
		sec = convert_period_into_seconds('4h')
		optimum = PoloniexHttpAPI.optimum_period(sec)
		self.assertEqual(optimum, 14400)

	def test_optimum_period_for_1d(self):
		sec = convert_period_into_seconds('1d')
		optimum = PoloniexHttpAPI.optimum_period(sec)
		self.assertEqual(optimum, 86400)

