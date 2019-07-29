import unittest2 as unittest

from utils import validate_period_format, convert_period_into_seconds, convert_period_into_pandas_freq

class TestUtils(unittest.TestCase):

	def test_period_is_valid(self):
		valid = validate_period_format('25m')
		self.assertTrue(valid)

	def test_period_is_invalid(self):
		valid = validate_period_format('1ah')
		self.assertFalse(valid)

	def test_period_in_hours_is_valid(self):
		valid = validate_period_format('3h')
		self.assertTrue(valid)

	def test_period_in_minutes_is_valid(self):
		valid = validate_period_format('27m')
		self.assertTrue(valid)

	def test_period_in_days_is_valid(self):
		valid = validate_period_format('20d')
		self.assertTrue(valid)

	def test_period_with_invalid_letter_is_invalid(self):
		valid = validate_period_format('14u')
		self.assertFalse(valid)

	def test_period_with_space_is_invalid(self):
		valid = validate_period_format('15 m')
		self.assertFalse(valid)

	def test_convert_5_minutes_into_seconds(self):
		sec = convert_period_into_seconds('5m')
		self.assertEqual(sec, 300)

	def test_convert_raises_value_error_if_minutes_not_multiple_of_5(self):
		with self.assertRaises(ValueError):
			convert_period_into_seconds('7m')

	def test_convert_25_minutes_into_seconds(self):
		sec = convert_period_into_seconds('25m')
		self.assertEqual(sec, 1500)

	def test_convert_2h_into_seconds(self):
		sec = convert_period_into_seconds('2h')
		self.assertEqual(sec, 7200)

	def test_convert_2d_into_seconds(self):
		sec = convert_period_into_seconds('2d')
		self.assertEqual(sec, 172800)

	def test_convert_invalid_value_into_seconds(self):
		with self.assertRaises(ValueError):
			sec = convert_period_into_seconds('abc')

	def test_convert_period_into_seconds_is_never_zero(self):
		sec = convert_period_into_seconds('155d')
		self.assertIsNot(sec, 0)

	def test_convert_period_in_minutes_into_pandas_frequency_format(self):
		freq = convert_period_into_pandas_freq('1m')
		self.assertEqual(freq, '1min')

	def test_convert_period_in_hours_into_pandas_frequency_format(self):
		freq = convert_period_into_pandas_freq('2h')
		self.assertEqual(freq, '2H')

	def test_convert_period_in_days_into_pandas_frequency_format(self):
		freq = convert_period_into_pandas_freq('5d')
		self.assertEqual(freq, '5D')
