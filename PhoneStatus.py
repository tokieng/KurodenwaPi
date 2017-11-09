# KurodenwaPi
# Copyright 2017 Yoshinori Tokimoto(tokieng)
# https://github.com/tokieng/KurodenwaPi
# MIT License

from enum import Enum

import Event

PhoneStatus = Enum("PhoneStatus", "NONE IDLE DIALING CALLING INCOMING TALKING BUNMEIDO DISCONNECTED SHUTDOWN ALARMSET ALARM")

class StatusBase:
	status_name = ''
	change_status = None

	def __init__(self, change_status):
		self.change_status = change_status

	def start(self, data = None):
		print("[I] Status[%s] start" % self.status_name)
		pass

	def end(self):
		print("[I] Status[%s] end" % self.status_name)
		pass

	def callback_offhook(self):
		return True

	def callback_onhook(self):
		return True

	def callback_dial_start(self):
		return True

	def callback_dial_end(self, dial):
		return True

	def callback_incoming(self, path):
		return True

	def callback_disconnected(self):
		return True

	def callback_alarm(self, hour, min):
		return False
