# KurodenwaPi
# Copyright 2017 Yoshinori Tokimoto(tokieng)
# https://github.com/tokieng/KurodenwaPi
# MIT License

import Event

class Alarm(Event.Base):
	hour = None
	min = None

	def __init__(self, hour, min):
		self.hour = hour
		self.min = min
