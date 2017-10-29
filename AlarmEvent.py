import Event

import AlarmEvent as Event

class AlarmEvent(Event.Base):
	timestr = None

	def __init__(self, timest):
		self.timestr = timestr
