from PhoneStatus import PhoneStatus
from PhoneStatus import StatusBase
import Event

import os
import subprocess

class StatusShutdown(StatusBase):
	p_sound = None

	def __init__(self, change_status):
		super().__init__(change_status)
		pass

	def start(self, data):
		super().start()
		dir = os.path.dirname(__file__)
		self.p_sound = subprocess.Popen(["paplay", "sound/shutdown.wav"])
		pass

	def end(self):
		super().end()
		if self.p_sound and self.p_sound.poll() == None:
			self.p_sound.kill()
		pass

	def callback_onhook(self):
		self.change_status(PhoneStatus.IDLE)
		subprocess.call("sudo shutdown -h now", shell=True)
		pass

if __name__ == '__main__':

	msg = "コレヨ'リ、シャットダ'ウンオ/カイシシマ'_ス。"
	msg += "<NUMK VAL=2 COUNTER=フン>ホド/マ'ッテカラ、デンゲンオ/ヌイテクダサ'イ。デンワオ/キ'ッテ、オマチクダ'サイ。"
	subprocess.Popen(["/home/pi/aquestalkpi/AquesTalkPi", "-o", "sound/shutdown.wav", "-k", msg] )
