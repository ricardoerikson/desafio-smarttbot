import sys
import requests
import pandas as pd

from app_bots import db, app
from currency_pairs_model import CurrencyPair
from flask_migrate import Migrate

Migrate(app, db)

with app.app_context():
	response = requests.get('http://chart_data:5000/currencies')
	if response.status_code != 200:
		sys.exit(1)

	db.create_all()
	currencies = []
	df = pd.read_json(response.content, orient='index')
	df.sort_index(ascending=True, inplace=True)
	for code, row in df.iterrows():
		currencies.append(CurrencyPair(int(row['id']), code))
	db.session.add_all(currencies)
	db.session.commit()