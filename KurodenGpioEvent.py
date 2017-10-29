import Event

class OnHook(Event.Base):
	pass

class OffHook(Event.Base):
	pass

class DialStart(Event.Base):
	pass

class DialEnd(Event.Base):
	dial = None

	def __init__(self, dial):
		self.dial = dial
