# KurodenwaPi
# Copyright 2017 Yoshinori Tokimoto(tokieng)
# https://github.com/tokieng/KurodenwaPi
# MIT License

# イベントディスパッチャー
import threading
import queue

import time

import Event
import KurodenGpioEvent as GpioEvent
import HFPEvent
import ScheduleEvent

class EventDispatcher:

	thread = None
	event_queue = None

	current_status = None
	statuses = {}

	def __init__(self):
		pass

	def start(self, statuses, init_status):
		self.statuses = statuses

		self.current_status = init_status
		self.statuses[init_status].start(None)

		if self.thread == None:
			self.event_queue = queue.Queue()
			self.thread = threading.Thread(target=self._main)
			self.thread.start()

	def end(self):
		self.event_queue.put(Event.End())
		self.thread.join()
		pass

	def _main(self):
		print("Dispacher thread start")

		while True:
			event = self.event_queue.get()
			type = event.__class__.__name__

			if type == 'End':
				break
			elif type == 'ChangeStatus':
#				print("* STATUS changed %s => %s" % (self.current_status, event.next) )
				self.statuses[self.current_status].end()
				self.statuses[event.next].start(event.data)
				self.current_status = event.next
			else:
				if self.current_status:
					print("* event process start type={0}".format(type))
					self._dispatch(event)
					print("* event process end")
				else:
					print("[D] ignore this event:", type)

			self.event_queue.task_done()
#			print("* dispacher idle")

		print("Dispacher thread end")

	def push(self, event):
		self.event_queue.put(event)

	def change_status(self, status, data=None):
#		print("Push Status: {0} -> {1}".format(self.current_status , status))
		event = Event.ChangeStatus(status, data)
		self.push(event)

	def _dispatch(self, event):
		statusobj = self.statuses[self.current_status]
		data = event.data

		result = True

		if isinstance(event, GpioEvent.OnHook):
			result = statusobj.callback_onhook()

		elif isinstance(event, GpioEvent.OffHook):
			result = statusobj.callback_offhook()

		elif isinstance(event, GpioEvent.DialStart):
			result = statusobj.callback_dial_start()

		elif isinstance(event, GpioEvent.DialEnd):
			result = statusobj.callback_dial_end(event.dial)

		# about HFP
		elif isinstance(event, HFPEvent.Incoming):
			path = event.path
			result = statusobj.callback_incoming(path)

		elif isinstance(event, HFPEvent.Disconnected):
			path = event.path
			result = statusobj.callback_disconnected()

		# about Alarm
		elif isinstance(event, ScheduleEvent.Alarm):
			result = statusobj.callback_alarm(event.hour, event.min)

		# try again
		if result == False:
			self.push(event)
