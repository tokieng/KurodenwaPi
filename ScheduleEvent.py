import Event

class Alarm(Event.Base):
	hour = None
	min = None

	def __init__(self, hour, min):
		self.hour = hour
		self.min = min
