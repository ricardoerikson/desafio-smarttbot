from main import app

from main.scheduler import sched

sched.start()

if __name__ == '__main__':
	app.run(debug=False, host='0.0.0.0')