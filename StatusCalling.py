# KurodenwaPi
# Copyright 2017 Yoshinori Tokimoto(tokieng)
# https://github.com/tokieng/KurodenwaPi
# MIT License

from PhoneStatus import PhoneStatus
from PhoneStatus import StatusBase

class StatusCalling(StatusBase):
	hfp = None
	calling_path = None

	def __init__(self, change_status, hfp, tone):
		self.status_name = __class__.__name__
		super().__init__(change_status)

		self.hfp = hfp

	def start(self, data):
		super().start()

		self.tel_number = data["tel"]
		print("Call to:'%s'" % (self.tel_number))
		self.hfp.call(self.tel_number)
		self.change_status(PhoneStatus.TALKING)

	def end(self):
		super().end()


	def callback_onhook(self):
		self.hfp.hangup()
		return True
