from PhoneStatus import PhoneStatus
from PhoneStatus import StatusBase
import Event

class StatusNone(StatusBase):

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
		print("callback_offhook")

	def callback_onhook(self):
		print("callback_onhook")

	def callback_dial_start(self):
		print("callback_dial_start")

	def callback_dial_end(self, dial):
		print("callback_dial_end: dial={0}".format(dial))

	def callback_dial_pulse(self, level):
		print("callback_dial_pulse")

	def callback_incoming(self, path):
		print("callback_incoming")
