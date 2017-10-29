from PhoneStatus import PhoneStatus
from PhoneStatus import StatusBase
import Event

class StatusIdle(StatusBase):

	def __init__(self, change_status):
		self.status_name = __class__.__name__
		super().__init__(change_status)
		pass

	def start(self, data):
		super().start()
		pass

	def end(self):
		super().end()
		pass


	def callback_offhook(self):
		self.change_status(PhoneStatus.DIALING)

	def callback_onhook(self):
		pass

	def callback_dial_start(self):
		pass

	def callback_dial_end(self, dial):
		pass

	def callback_incoming(self, path):
		data = { 'path': path }
		self.change_status(PhoneStatus.INCOMING, data)

	def callback_alarm(self, hour, min):
		print("** ALARM hour={0} min={1}".format(hour,min))
		data = { 'hour':hour, 'min':min }
		self.change_status(PhoneStatus.ALARM, data)
