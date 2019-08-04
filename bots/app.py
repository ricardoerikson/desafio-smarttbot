from main import app

from main.scheduler import sched

sched.start()

if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0')