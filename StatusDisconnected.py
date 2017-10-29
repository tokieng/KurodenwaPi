from PhoneStatus import PhoneStatus
from PhoneStatus import StatusBase
import Tone

class StatusDisconnected(StatusBase):
	tone = None

	def __init__(self, change_status, tone):
		self.status_name = __class__.__name__
		super().__init__(change_status)
		self.tone = tone

	def start(self, data):
		super().start()
		self.tone.play(Tone.Type.BUSY)

	def end(self):
		super().end()
		self.tone.stop()


	def callback_onhook(self):
		self.change_status(PhoneStatus.IDLE)
		return True

	# 受話器上がってるから、ほんとは相手に話中を伝えたい
	def callback_incoming(self, path):
		return True
