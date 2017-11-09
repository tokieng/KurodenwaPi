# KurodenwaPi
# Copyright 2017 Yoshinori Tokimoto(tokieng)
# https://github.com/tokieng/KurodenwaPi
# MIT License

import dbus
import dbus.mainloop.glib

import HFPEvent as Event

class HFP:
	push_event = None

	call_path = None
	incoming_path = None

	bus = None
	modem = None

	def __init__(self, push_event):
		dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
		bus = dbus.SystemBus()
		manager = dbus.Interface(bus.get_object('org.ofono', '/'),
								'org.ofono.Manager')
		modems = manager.GetModems()

		modem_path = modems[0][0]
#		for modem in modems:
#			if modem[1]['Powered'] == True:
#				modem_path = modem[0]
#				break

		if modem_path == None:
			# TODO
			raise Exception()

		print("Using modem %s" % modem_path)

		bus.add_signal_receiver(
			self.callback_property_changed,
			bus_name="org.ofono",
			signal_name = "PropertyChanged",
			path_keyword="path",
			interface_keyword="interface")

		bus.add_signal_receiver(
			self.callback_added,
			bus_name="org.ofono",
			signal_name = "CallAdded",
			member_keyword="member",
			path_keyword="path",
			interface_keyword="interface")

		bus.add_signal_receiver(
			self.callback_removed,
			bus_name="org.ofono",
			signal_name = "CallRemoved",
			member_keyword="member",
			path_keyword="path",
			interface_keyword="interface")

		self.bus = bus
		self.modem = modem_path
		self.push_event = push_event

	def call(self, tel_number):
		vcm = dbus.Interface(self.bus.get_object('org.ofono', self.modem),
								'org.ofono.VoiceCallManager')
		self.call_path = vcm.Dial(tel_number, "default")

	def answer(self):
		call = dbus.Interface(self.bus.get_object('org.ofono', self.incoming_path),
								'org.ofono.VoiceCall')
		call.Answer()
		self.call_path = self.incoming_path
		self.incoming_path = None

	def hangup(self):
		if self.call_path:
			call = dbus.Interface(self.bus.get_object('org.ofono', self.call_path),
									'org.ofono.VoiceCall')
			call.Hangup()
		else:
			print("Call is not exist")
		self.call_path = None
		self.incoming_path = None

	def callback_property_changed(self, name, value, path, interface):
		#print("*property_changed*",name,value,path,interface)
		pass

	def callback_added(self, name, value, member, path, interface):
		if value["State"] == 'incoming':
			self.incoming_path = name
			self.push_event(Event.Incoming(name))
		elif value["State"] == 'active':
			self.push_event(Event.Active(name))

	def callback_removed(self, name, member, path, interface):
		#print("name={0} member={1} path={2} interface={3}", name, member, path, interface)
		#print("HFP: disconnected")
		self.push_event(Event.Disconnected(name))
		self.call_path = None
		self.incoming_path = None

	def sendTone(self,digit):
		list = {
			0:'0', 1:'1', 2:'2', 3:'3', 4:'4', 5:'5', 6:'6', 7:'7', 8:'8', 9:'9', 10:'*'
		}
		vcm = dbus.Interface(self.bus.get_object('org.ofono', self.modem),
							'org.ofono.VoiceCallManager')
		vcm.SendTones(list[digit])
