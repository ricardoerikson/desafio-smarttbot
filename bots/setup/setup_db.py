import sys
import requests
import pandas as pd

sys.path.append('/bots')

from main import app, db
from main.currencies.models import CurrencyPair

with app.app_context():
	response = requests.get('http://chart_data:5000/currencies')
	if response.status_code != 200:
		sys.exit(1)

	currencies = []
	df = pd.read_json(response.content, orient='index')
	df.sort_index(ascending=True, inplace=True)
	for code, row in df.iterrows():
		currencies.append(CurrencyPair(int(row['id']), code))
	db.session.add_all(currencies)
	db.session.commit()