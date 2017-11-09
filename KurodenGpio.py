# KurodenwaPi
# Copyright 2017 Yoshinori Tokimoto(tokieng)
# https://github.com/tokieng/KurodenwaPi
# MIT License

import pigpio
from enum import Enum
import time
import threading
from threading import Timer

import KurodenGpioEvent as Event

#####

HIGH = 1
LOW = 0

PORT_DIALING = 22
PORT_DIAL_PULSE = 17
PORT_HOOK = 24

PORT_COIL_POWER = 10
PORT_COIL_OUT1 = 5
PORT_COIL_OUT2 = 13
#WAIT_COIL = 0.07
WAIT_COIL = 0.05

class KurodenGpio:
	Status = Enum("Status", "IDLE WAIT_PULSE PULSE_HIGH PULSE_LOW")

	gpio = None
	push_event = None

	status = Status.IDLE
	dial_count = 0
	tel_number = ""

	thread = None
	event_thread_stop = None

	timer_hook = None

	def __init__(self, push_event):
		gpio = pigpio.pi()
		# Power On for coil
		gpio.set_mode (PORT_COIL_POWER, pigpio.OUTPUT)
		gpio.write(PORT_COIL_POWER, LOW)

		gpio.set_mode (PORT_DIAL_PULSE, pigpio.INPUT)
		gpio.set_mode (PORT_DIALING, pigpio.INPUT)
		gpio.set_mode (PORT_HOOK, pigpio.INPUT)

		gpio.set_glitch_filter(PORT_DIAL_PULSE, 1000)
		gpio.set_glitch_filter(PORT_DIALING, 1000)
		gpio.set_glitch_filter(PORT_HOOK, 1000)

		gpio.callback(PORT_DIAL_PULSE, pigpio.EITHER_EDGE, self.callback_gpio_d_ramda)
		gpio.callback(PORT_DIALING,    pigpio.EITHER_EDGE, self.callback_gpio_d_i)
		gpio.callback(PORT_HOOK,       pigpio.EITHER_EDGE, self.callback_gpio_hook)

		self.gpio = gpio
		self.push_event = push_event
		self.ring_single(1) # 1回 or 2回、鳴る。次の鳴動がちゃんとできるように。

	def __del__(self):
		self.ring_single(1) # 終了を知らせる
		self.gpio.write(PORT_COIL_POWER, LOW)
		self.gpio.stop()

	def _cancel_timer(self):
		if self.timer_hook is not None:
			self.timer_hook.cancel()
			self.timer_hook = None

	def proc_onhook(self):
		self.push_event(Event.OnHook())
		self._cancel_timer()

	def callback_gpio_hook(self, gpio, level, tick):

		if level == 0:
			if self.timer_hook is not None:
				self._cancel_timer()
				self.push_event(Event.DialEnd(10))
			else:
				self.push_event(Event.OffHook())
		else:
			self.timer_hook = Timer(0.5, self.proc_onhook)
			self.timer_hook.start()

	def callback_gpio_d_i(self, gpio, level, tick):
		if level == 0:
			self.push_event(Event.DialStart())
			if self.status == self.Status.IDLE:
				self.status = self.Status.WAIT_PULSE
				self.dial_count = 0
		else:
			if self.status == self.Status.PULSE_LOW or self.status == self.Status.WAIT_PULSE:
				self.status = self.Status.IDLE
				if self.dial_count != 0:
					if self.dial_count == 10:
						self.dial_count = 0
					print("** input:", self.dial_count)
					self.push_event(Event.DialEnd(self.dial_count))

	def callback_gpio_d_ramda(self, gpio, level, tick):
		if level == 1 and (self.status == self.Status.WAIT_PULSE or self.status == self.Status.PULSE_LOW):
			self.status = self.Status.PULSE_HIGH
		elif level == 0 and self.status == self.Status.PULSE_HIGH:
			self.status = self.Status.PULSE_LOW
			self.dial_count += 1

	def ring_power_on(self):
		self.gpio.write(PORT_COIL_POWER, HIGH)

	def ring_power_off(self):
		self.gpio.write(PORT_COIL_POWER, LOW)

	ring_pins = [PORT_COIL_OUT1, PORT_COIL_OUT2]
	def ring_single(self, times=1):
		pins = self.ring_pins
		gpio = self.gpio
		for i in range(0, times):
			gpio.write(pins[0], HIGH)
			time.sleep(WAIT_COIL)
			gpio.write(pins[0], LOW)
			pins[0], pins[1] = pins[1], pins[0]  # swap

	def ring_start(self, type=1):
		self.event_thread_stop = threading.Event()
		self.thread = threading.Thread(target=self._ringer_thread, args=(type,))

		self.thread.start()

	def ring_end(self):
		if self.event_thread_stop:
			self.event_thread_stop.set()
		if self.thread:
			self.thread.join()
		self.event_thread_stop = None
		self.thread = None

	def _ringer_thread(self, type):
		def r1():
			self.ring_single(2)
		def sleep():
			time.sleep(0.5)
		def sleep_s():
			time.sleep(0.1)

		if type == 2:
			func = [ r1, r1,
			         sleep_s,
			         r1, r1,
			         sleep, sleep, sleep, sleep ]
		else:
			func = [ r1, r1, r1, r1, r1, r1, r1, r1, r1, r1, 
			         sleep, sleep, sleep, sleep ]

		i = 0
		while not self.event_thread_stop.is_set():
			func[i]()
			i = i+1 if i < len(func)-1 else 0
		gpio = self.gpio
		gpio.write(PORT_COIL_OUT1, LOW)
		gpio.write(PORT_COIL_OUT2, LOW)

#####
def _dummy_push_event():
	pass

if __name__ == '__main__':
	print("** START **")
	gpio = KurodenGpio(_dummy_push_event)
	time.sleep(3)
	print("** START 2 **")
	gpio.ring_start(3)
	time.sleep(20)
	gpio.ring_end()
