from flask import Blueprint, redirect, url_for

home_blueprint = Blueprint('home', __name__, static_folder='static', template_folder='templates')

@home_blueprint.route('/', methods=['GET'])
@home_blueprint.route('/home', methods=['GET'])
@home_blueprint.route('/index', methods=['GET'])
def index():
	return redirect(url_for('currencies.index'))