# KurodenwaPi
# Copyright 2017 Yoshinori Tokimoto(tokieng)
# https://github.com/tokieng/KurodenwaPi
# MIT License

import subprocess
from enum import Enum
import os

Type = Enum("Type", "TONE RINGBACK BUSY")

class Tone:

	is_playing = False
	proc = None

	def __init__(self):
		self.dir = os.path.dirname(__file__)
		pass

	def __del__(self):
		self.stop()
		pass

	def play(self, type):
		file = {
			Type.TONE: self.dir + "/sound/tone.wav",
			Type.RINGBACK: self.dir + "/sound/ringback.wav",
			Type.BUSY: self.dir + "/sound/busy.wav",
		}
		self.is_playing = True
		print("FILE={0}".format(file[type]))
		self.proc = subprocess.Popen([ "paplay", file[type] ])
		pass

	def stop(self):
		if self.proc and self.proc.poll() == None:
			self.proc.kill()
		if self.is_playing:
			pass
		self.is_playing = False

	def is_playing(self):
		return is_playing
