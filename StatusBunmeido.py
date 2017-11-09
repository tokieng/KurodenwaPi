# KurodenwaPi
# Copyright 2017 Yoshinori Tokimoto(tokieng)
# https://github.com/tokieng/KurodenwaPi
# MIT License

from PhoneStatus import PhoneStatus
from PhoneStatus import StatusBase
import Event

import subprocess
import os

class StatusBunmeido(StatusBase):
	p_bunmeido = None

	def __init__(self, change_status):
		self.status_name = __class__.__name__
		super().__init__(change_status)
		pass

	def start(self, data):
		super().start()
		self.p_bunmeido = subprocess.Popen(["paplay", os.path.dirname(__file__) + "/sound/bunmeido.wav"])
		pass

	def end(self):
		super().end()
		if self.p_bunmeido and self.p_bunmeido.poll() == None:
			self.p_bunmeido.kill()
		pass


	def callback_onhook(self):
		if self.p_bunmeido and self.p_bunmeido.poll() == None:
			self.p_bunmeido.kill()
		self.change_status(PhoneStatus.IDLE)
		return True

	def callback_incoming(self, path):
		self.change_status(PhoneStatus.INCOMING)
		return True
