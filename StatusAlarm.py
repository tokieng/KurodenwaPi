from PhoneStatus import PhoneStatus
from PhoneStatus import StatusBase

import subprocess

class StatusAlarm(StatusBase):
	gpio = None
	p_wavplay = None
	hour = None
	min = None

	def __init__(self, change_status, gpio):
		self.status_name = __class__.__name__
		super().__init__(change_status)
		self.gpio = gpio

	def start(self, data):
		super().start()
		p_wavplay = None
		self.hour = data["hour"]
		self.min = data["min"]
		self.gpio.ring_power_on()
		self.gpio.ring_start(type=2)
		print("リーン リーン リーン...")

	def end(self):
		super().end()
		self.gpio.ring_end()
		self.gpio.ring_power_off()
		self.p_wavplay.kill()

	def callback_offhook(self):
		self.gpio.ring_end()
		self.gpio.ring_power_off()

		self.makewav(self.hour, self.min)

		return True

	def callback_onhook(self):
		self.change_status(PhoneStatus.IDLE)
		return True

	def callback_incoming(self, path):
		self.change_status(PhoneStatus.INCOMING)
		return True

	def makewav(self, hour, min):
		if min == 0:
			minstr = "ちょう;ど"
		else:
			minstr = "<NUMK VAL=" + str(min) + " COUNTER=ふん>"

		msg  = "オハヨウ/ゴザイ/マ_ス。";
		msg += "<NUMK VAL="+ str(hour) + " COUNTER=ジ>、" + minstr + "デ_ス。";
		msg += "オメザメワ,イカ'ガデ_スカ？。ド'ーゾ/キョ'ーモ、ヨ'イ;イチニチ/デ+アリマス;ヨ'ウニ。。ゴリヨウ;アリガトウ/ゴザイマ'シタ。"
		subprocess.call(["/home/pi/aquestalkpi/AquesTalkPi", "-k", "-o", "/tmp/hfpclient_tmp.wav", msg])
		self.p_wavplay = subprocess.Popen(["paplay", "/tmp/hfpclient_tmp.wav"])

if __name__ == '__main__':

	hour = 7
	min = 1

	change_status = None
	gpio = None
	a = StatusAlarm(change_status, gpio)
	a.makewav(hour, min)
