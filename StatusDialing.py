# KurodenwaPi
# Copyright 2017 Yoshinori Tokimoto(tokieng)
# https://github.com/tokieng/KurodenwaPi
# MIT License

from PhoneStatus import PhoneStatus
from PhoneStatus import StatusBase
import Event
import Tone

from enum import Enum
from threading import Timer


import threading  # get thread id

class StatusDialing(StatusBase):

	Status = Enum("Status", "IDLE WAIT_PULSE PULSE_HIGH PULSE_LOW")

	status = Status.IDLE
	tel_number = ""
	timer_dial = None
	bus = None
	modem = None

	def __init__(self, change_status, tone):
		self.status_name = __class__.__name__
		super().__init__(change_status)

		self.tone = tone

	def start(self, data):
		super().start()
		self.tel_number = ""

		print("ツー...")
		self.tone.play(Tone.Type.TONE)

	def end(self):
		super().end()
		self.tone.stop()

	def callback_onhook(self):
		self.tone.stop()
		if self.timer_dial is not None:
			self.timer_dial.cancel()

		print("ガチャッ")
		self.change_status(PhoneStatus.IDLE)
		return True

	def callback_dial_start(self):
		self.tone.stop()
		if self.timer_dial is not None:
			self.timer_dial.cancel()
			self.timer_dial = None
		return True

	def callback_dial_end(self, dial):
		self.tel_number += str(dial)
		self.timer_dial = Timer(3, self.proc_dial)
		self.timer_dial.start()
		print("** input:", self.tel_number)
		return True

	def proc_dial(self):
		if self.tel_number == '2':
			self.change_status(PhoneStatus.BUNMEIDO)
		elif self.tel_number == '7':
			self.change_status(PhoneStatus.ALARMSET)
		elif self.tel_number == '9':
			self.change_status(PhoneStatus.SHUTDOWN)
		else:
			self.exec_dial()

	def exec_dial(self):
		if self.tel_number == '5':
			self.tel_number = '03177'
		print("Call to:'{0}'".format(self.tel_number))
		data = { 'tel':self.tel_number }
		self.change_status(PhoneStatus.CALLING, data)
