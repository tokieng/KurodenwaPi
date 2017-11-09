# KurodenwaPi
# Copyright 2017 Yoshinori Tokimoto(tokieng)
# https://github.com/tokieng/KurodenwaPi
# MIT License

from PhoneStatus import PhoneStatus
from PhoneStatus import StatusBase

class StatusTalking(StatusBase):
	hfp = None

	def __init__(self, change_status, hfp):
		self.status_name = __class__.__name__
		super().__init__(change_status)

		self.hfp = hfp

	def start(self, data):
		super().start()

	def end(self):
		super().end()

	def callback_dial_end(self, dial):
		self.hfp.sendTone(dial)

	def callback_onhook(self):
		self.hfp.hangup()
		self.change_status(PhoneStatus.IDLE)

	def callback_disconnected(self):
		print("ガチャン。ツー、ツー、ツー・・・")
		self.change_status(PhoneStatus.DISCONNECTED)
