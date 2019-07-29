import re

def validate_period_format(period_str):
	"""validates a period in string format

	Args:
	    period_str (string): period in string format starting with a
	    number and ending with the letters m, h or d, for minutes, hour and day,
	    respectively.

	Returns:
	    bool: True if the period is valid, else False
	"""
	regex = r"^[0-9]+[hmd]$"
	result = re.search(regex, period_str, re.MULTILINE)
	return False if result is None else True

def convert_period_into_seconds(period_str):
	"""converts a given period of time (in string format) into seconds

	Args:
	    period_str (string): period of time represented by a number followed by either
	    of the letters 'm', 'h' or 'd', corresponding to minutes, hour and day, respectively.

	Returns:
	    int: period of time in seconds

	Raises:
	    ValueError: raised if the period is represented in minutes and it's not a multiple of 5.
	"""
	number = int(''.join(filter(str.isdigit, period_str)))
	letter = ''.join(filter(str.isalpha, period_str))

	if (letter is 'm') and (number % 5 is not 0):
		raise ValueError('If you are using "minutes", the period must be multiple of 5.')

	if letter is 'm':
		return number * 60
	if letter is 'h':
		return number * 60 * 60

	# if period is given in days (d)
	return number * 60 * 60 * 24

def convert_period_into_pandas_freq(period_str):
	"""converts the period into a frequency format used by pandas library.

	Args:
	    period_str (string): period in string format using m, h and d to represent
	    minutes, hours and days.

	Returns:
	    string: new value for period according to pandas frequency format.
	    ex: 1m -> 1min, 1h -> 1H and 1d -> 1D
	"""
	number = ''.join(filter(str.isdigit, period_str))
	letter = ''.join(filter(str.isalpha, period_str))
	if letter == 'm':
		return ''.join([number, 'min'])
	# return uppercase of period_str for other values of letter
	return period_str.upper()