import pandas as pd
import requests

from flask import Blueprint, render_template

currencies_blueprint = Blueprint('currencies', __name__, template_folder='templates')

@currencies_blueprint.route('/', methods=['GET'])
def index():
	url = 'http://chart_data:5000/ticker'
	res = requests.get(url)
	df = pd.read_json(res.content, orient='index')
	df = df.reindex(columns=['last', 'percentChange', 'high24hr', 'low24hr', 'baseVolume'])
	df['font_color'] = df['percentChange'].map(lambda v: 'text-secondary' if v == 0 else ('text-success' if v > 0 else 'text-danger'))
	df.sort_index(ascending=True, inplace=True)
	return render_template('currencies/index.html', df=df)

