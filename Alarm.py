import AlarmEvent as Event

class Alarm:
	push_event = None

	def __init__(self, push_event):
		self.push_event = push_event

