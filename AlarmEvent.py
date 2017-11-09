# KurodenwaPi
# Copyright 2017 Yoshinori Tokimoto(tokieng)
# https://github.com/tokieng/KurodenwaPi
# MIT License

import Event

import AlarmEvent as Event

class AlarmEvent(Event.Base):
	timestr = None

	def __init__(self, timest):
		self.timestr = timestr
