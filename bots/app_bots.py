from flask import Flask

app = Flask(__name__)

@app.route('/index2')
def index2():
	return '<h1>This is index2!:</h1><h2>Ricardo Erikson</h2>'

@app.route('/index')
def index():
	return '<h1>This is index</h1><h2>Ricardo Erikson</h2>'


if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0')