# KurodenwaPi
# Copyright 2017 Yoshinori Tokimoto(tokieng)
# https://github.com/tokieng/KurodenwaPi
# MIT License

class Base():
	data = None

	def __init__(self, data=None):
		self.data = data


class End(Base):
	pass

class ChangeStatus(Base):
	next = None

	def __init__(self, next, data=None):
		super().__init__(data)
		self.next = next
