# KurodenwaPi
# Copyright 2017 Yoshinori Tokimoto(tokieng)
# https://github.com/tokieng/KurodenwaPi
# MIT License

import AlarmEvent as Event

class Alarm:
	push_event = None

	def __init__(self, push_event):
		self.push_event = push_event

