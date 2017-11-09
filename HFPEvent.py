# KurodenwaPi
# Copyright 2017 Yoshinori Tokimoto(tokieng)
# https://github.com/tokieng/KurodenwaPi
# MIT License

import Event

class Incoming(Event.Base):
	path = None

	def __init__(self, path):
		self.path = path


class Active(Event.Base):
	path = None

	def __init__(self, path):
		self.path = path

class Disconnected(Event.Base):
	path = None

	def __init__(self, path):
		self.path = path
