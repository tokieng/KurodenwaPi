# KurodenwaPi
# Copyright 2017 Yoshinori Tokimoto(tokieng)
# https://github.com/tokieng/KurodenwaPi
# MIT License

from PhoneStatus import PhoneStatus
from PhoneStatus import StatusBase
import Event
import Tone
import Schedule

import subprocess
import os

class StatusAlarmSet(StatusBase):
	p_sound = None
	set_hour = 0
	set_min = 0
	dial_count = 0
	gpio = None
	tone = None
	schedule = None

	def __init__(self, change_status, schedule, gpio, tone):
		self.status_name = __class__.__name__
		super().__init__(change_status)
		self.gpio = gpio
		self.tone = tone
		self.schedule = schedule

		msg_common = "オメザメニナリタイジコ'クオ、ヨン'ケタデ、ニューリョクシテクダ'サイ。"
		msg_common += "タト'エバ、ゴ'ゼン、ヒチ'ジ、サンジュップン/ノ/バ'アイワ、"
		msg_common += "ゼ'ロ、ナ'ナ、サン、ゼ'ロ、ト/ダイヤル/シテ/クダ'サイ。"

		self.msg_first = "モーニングコ'ールノ/セッテイオ/カイシシマ'_ス。" + msg_common

		self.msg_retry = "ニューリョクニ/アヤマリ'ガ/アリ'マス.サ'イド/ニューリョク_シテクダサ'イ。"
		self.msg_retry += msg_common

	def start(self, data):
		super().start()
		dir = os.path.dirname(__file__)
		self.dir_sound = dir + "/sound/"
		self.set_hour = 0
		self.set_min = 0
		self.dial_count = 0

		subprocess.call(["/home/pi/aquestalkpi/AquesTalkPi", "-o", "/tmp/hfpclient_tmp.wav", "-k", self.msg_first] )
		self.p_sound = subprocess.Popen(["paplay", "/tmp/hfpclient_tmp.wav"])

	def end(self):
		super().end()
		if self.p_sound and self.p_sound.poll() == None:
			self.p_sound.kill()

	def callback_offhook(self):
		return True

	def callback_onhook(self):
		if self.p_sound and self.p_sound.poll() == None:
			self.p_sound.kill()
		#self.gpio.ring_single()
		self.change_status(PhoneStatus.IDLE)
		return True

	def callback_dial_start(self):
		if self.p_sound and self.p_sound.poll() == None:
			self.p_sound.kill()
		return True

	def callback_dial_end(self, dial):

		print("*DIAL={0}".format(dial))
		if self.dial_count == 0:
			self.set_hour = dial * 10;
			self.dial_count = 1
		elif self.dial_count == 1:
			self.set_hour += dial;
			self.dial_count = 2
		elif self.dial_count == 2:
			self.set_min = dial * 10;
			self.dial_count = 3
		elif self.dial_count == 3:
			self.set_min += dial;
			self.dial_count = 4
		elif self.dial_count == 4:
			self.dial_count = 5

		print("*** HOUR={0} MIN={1}".format(self.set_hour,self.set_min))

		if self.dial_count == 4:
			if (0 <= self.set_hour <= 24) and (0 <= self.set_min <= 59):
				if self.set_min == 0:
					minstr = "ちょう'ど"
				else:
					minstr = "<NUMK VAL=" + str(self.set_min) + " COUNTER=ふん>"
				msg  = "<NUMK VAL=" + str(self.set_hour) + " COUNTER=じ>." + minstr + ".ニ/セッテイシテ/ヨロシ'イデスカ？"
				msg += "。ヨロシ'ケレバ、イ_チ'、オ、ニューリョクオ、ヤリナオ'ス+ト'キワ、ゼ'ロ、オ、ダイヤルシテクダサ'イ。"
				subprocess.call(["/home/pi/aquestalkpi/AquesTalkPi", "-o", "/tmp/hfpclient_tmp.wav", "-k", msg])
				self.p_sound = subprocess.Popen(["paplay", "/tmp/hfpclient_tmp.wav"])
			else:
				self.dial_count = 0
				self.set_hour = 0
				self.set_min = 0
				subprocess.call(["/home/pi/aquestalkpi/AquesTalkPi", "-o", "/tmp/hfpclient_tmp.wav", "-k", self.msg_retry])
				self.p_sound = subprocess.Popen(["paplay", "/tmp/hfpclient_tmp.wav"])

		if self.dial_count == 5:
			if dial == 1:
				self.schedule.start(self.set_hour, self.set_min)

				if self.set_min == 0:
					minstr = "ちょう'ど"
				else:
					minstr = "<NUMK VAL=" + str(self.set_min) + " COUNTER=ふん>"
				msg  = "<NUMK VAL=" + str(self.set_hour) + " COUNTER=じ>." + minstr + ".ニ/セッテイしま'した。デンワオ/オキリクダサ'イ。"
				subprocess.call(["/home/pi/aquestalkpi/AquesTalkPi", "-k", "-o", "/tmp/hfpclient_tmp.wav", msg])
				self.p_sound = subprocess.Popen(["paplay", "/tmp/hfpclient_tmp.wav"])
			elif dial == 0:
				self.dial_count = 0
				self.set_hour = 0
				self.set_min = 0
				subprocess.call(["/home/pi/aquestalkpi/AquesTalkPi", "-o", "/tmp/hfpclient_tmp.wav", "-k", self.msg_first])
				self.p_sound = subprocess.Popen(["paplay", "/tmp/hfpclient_tmp.wav"])
		return True

	def callback_incoming(self, path):
		self.change_status(PhoneStatus.INCOMING)
		return True
