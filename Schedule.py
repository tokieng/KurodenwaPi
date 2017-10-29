from datetime import datetime, timedelta
import threading

import ScheduleEvent as Event

class Schedule:
	push_event = None
	hour = None
	min = None
	timer = None

	def __init__(self, push_event):
		self.push_event = push_event

	def __del__(self):
		if self.timer:
			self.timer.cancel()

	def start(self, hour, min):
		self.cancel()
		self.hour = hour
		self.min = min
		t1 = datetime.today()
		t2 = t1.replace( hour=hour, minute=min, second=0)
		if t1 > t2:
			t2 += timedelta(1)

		seconds = (t2 - t1).total_seconds()
		print("sleep={0}".format(seconds))

		t = threading.Timer(seconds, self.fire)
		t.start()
		self.timer = t

	def cancel(self):
		if self.timer:
			self.timer.cancel()
			self.timer = None

	def fire(self):
		print("** TIME is come **")
		self.timer = None
		self.push_event(Event.Alarm(self.hour, self.min))

# test
if __name__ == '__main__':
	import time
	hour = 22
	min = 13

	def mock_push_event(e):
		if e.hour == hour:
			print("hour ok")
		else:
			print("hour ng")

		if e.min == min:
			print("min ok")
		else:
			print("min ng")

	schedule = Schedule(mock_push_event)
	schedule.start(hour, min)
	
	time.sleep(1000)
