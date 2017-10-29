from PhoneStatus import PhoneStatus
from PhoneStatus import StatusBase

class StatusIncoming(StatusBase):
	hfp = None
	gpio = None

	def __init__(self, change_status, hfp, gpio):
		self.status_name = __class__.__name__
		super().__init__(change_status)
		self.hfp = hfp
		self.gpio = gpio

	def start(self, data):
		super().start()
		self.gpio.ring_power_on()
		self.gpio.ring_start()
		print("リーン リーン リーン...")

	def end(self):
		super().end()
		self.gpio.ring_end()
		self.gpio.ring_power_off()

	def callback_offhook(self):
		self.gpio.ring_end()
		self.gpio.ring_power_off()
		self.hfp.answer()
		self.change_status(PhoneStatus.TALKING)
		return True

	def callback_disconnected(self):
		self.change_status(PhoneStatus.IDLE)
		return True
