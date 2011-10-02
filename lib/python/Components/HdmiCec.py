import struct
import os
from config import config, ConfigSelection, ConfigYesNo, ConfigSubsection, ConfigText
from enigma import eHdmiCEC
from Tools.DreamboxHardware import getFPWasTimerWakeup

config.hdmicec = ConfigSubsection()
config.hdmicec.enabled = ConfigYesNo(default = True)
config.hdmicec.control_tv_standby = ConfigYesNo(default = True)
config.hdmicec.control_tv_wakeup = ConfigYesNo(default = True)
config.hdmicec.report_active_source = ConfigYesNo(default = True)
config.hdmicec.report_active_menu = ConfigYesNo(default = True)
config.hdmicec.handle_tv_standby = ConfigYesNo(default = True)
config.hdmicec.handle_tv_wakeup = ConfigYesNo(default = True)
config.hdmicec.tv_wakeup_detection = ConfigSelection(
	choices = {
	"wakeup": _("Wakeup"),
	"sourcerequest": _("Source request"),
	"streamrequest": _("Stream request"),
	"osdnamerequest": _("OSD name request"),
	"activity": _("Any activity"),
	},
	default = "streamrequest")
config.hdmicec.fixed_physical_address = ConfigText(default = "0.0.0.0")
config.hdmicec.handle_deepstandby_events = ConfigYesNo(default = False)

class HdmiCec:
	def __init__(self):

		eHdmiCEC.getInstance().messageReceived.get().append(self.messageReceived)
		config.misc.standbyCounter.addNotifier(self.onEnterStandby, initial_call = False)
		self.setFixedPhysicalAddress(config.hdmicec.fixed_physical_address.value)
		
		if config.hdmicec.handle_deepstandby_events.value:
			if not getFPWasTimerWakeup():
				self.wakeupMessages()

	def getPhysicalAddress(self):
		physicaladdress = eHdmiCEC.getInstance().getPhysicalAddress()
		hexstring = '%04x' % physicaladdress
		return hexstring[0] + '.' + hexstring[1] + '.' + hexstring[2] + '.' + hexstring[3]

	def setFixedPhysicalAddress(self, address):
		if address != config.hdmicec.fixed_physical_address.value:
			config.hdmicec.fixed_physical_address.value = address
			config.hdmicec.fixed_physical_address.save()
		hexstring = address[0] + address[2] + address[4] + address[6]
		eHdmiCEC.getInstance().setFixedPhysicalAddress(int(float.fromhex(hexstring)))

	def sendMessage(self, address, message):
		cmd = 0
		data = ''
		if message == "wakeup":
			cmd = 0x04
		elif message == "sourceactive":
			address = 0x0f # use broadcast for active source command
			cmd = 0x82
			physicaladdress = eHdmiCEC.getInstance().getPhysicalAddress()
			data = str(struct.pack('BB', int(physicaladdress/256), int(physicaladdress%256)))
		elif message == "standby":
			cmd = 0x36
		elif message == "sourceinactive":
			address = 0x0f # use broadcast for inactive source command
			physicaladdress = eHdmiCEC.getInstance().getPhysicalAddress()
			cmd = 0x9d
			data = str(struct.pack('BB', int(physicaladdress/256), int(physicaladdress%256)))
		elif message == "menuactive":
			cmd = 0x8e
			data = str(struct.pack('B', 0x00))
		elif message == "menuinactive":
			cmd = 0x8e
			data = str(struct.pack('B', 0x01))
		elif message == "osdname":
			cmd = 0x47
			data = os.uname()[1]
			data = data[:14]
		elif message == "poweractive":
			cmd = 0x90
			data = str(struct.pack('B', 0x00))
		elif message == "powerinactive":
			cmd = 0x90
			data = str(struct.pack('B', 0x01))
		elif message == "reportaddress":
			address = 0x0f # use broadcast address
			cmd = 0x84
			physicaladdress = eHdmiCEC.getInstance().getPhysicalAddress()
			devicetype = eHdmiCEC.getInstance().getDeviceType()
			data = str(struct.pack('BBB', int(physicaladdress/256), int(physicaladdress%256), devicetype))
		elif message == "vendorid":
			cmd = 0x87
			data = '\x00\x00\x00'
		if cmd:
			eHdmiCEC.getInstance().sendMessage(address, cmd, data, len(data))

	def sendMessages(self, address, messages):
		for message in messages:
			self.sendMessage(address, message)

	def wakeupMessages(self):
		if config.hdmicec.enabled.value:
			messages = []
			if config.hdmicec.control_tv_wakeup.value:
				messages.append("wakeup")
			if config.hdmicec.report_active_source.value:
				messages.append("sourceactive")
			if config.hdmicec.report_active_menu.value:
				messages.append("menuactive")
			if messages:
				self.sendMessages(0, messages)

	def standbyMessages(self):
		if config.hdmicec.enabled.value:
			messages = []
			if config.hdmicec.control_tv_standby.value:
				messages.append("standby")
			else:
				if config.hdmicec.report_active_source.value:
					messages.append("sourceinactive")
				if config.hdmicec.report_active_menu.value:
					messages.append("menuinactive")
			if messages:
				self.sendMessages(0, messages)


	def onLeaveStandby(self):
		self.wakeupMessages()

	def onEnterStandby(self, configElement):
		from Screens.Standby import inStandby
		inStandby.onClose.append(self.onLeaveStandby)
		self.standbyMessages()

	def standby(self):
		from Screens.Standby import Standby, inStandby
		if not inStandby:
			from Tools import Notifications
			Notifications.AddNotification(Standby)

	def wakeup(self):
		from Screens.Standby import Standby, inStandby
		if inStandby:
			inStandby.Power()

	def messageReceived(self, message):
		if config.hdmicec.enabled.value:
			from Screens.Standby import inStandby
			cmd = message.getCommand()
			data = 16 * '\x00'
			length = message.getData(data, len(data))
			if cmd == 0x46: # request name
				self.sendMessage(message.getAddress(), 'osdname')
			elif cmd == 0x8f: # request power status
				if inStandby:
					self.sendMessage(message.getAddress(), 'powerinactive')
				else:
					self.sendMessage(message.getAddress(), 'poweractive')
			elif cmd == 0x83: # request address
				self.sendMessage(message.getAddress(), 'reportaddress')
			elif cmd == 0x86: # request streaming path
				physicaladdress = ord(data[0]) * 256 + ord(data[1])
				ouraddress = eHdmiCEC.getInstance().getPhysicalAddress()
				if physicaladdress == ouraddress:
					if not inStandby:
						if config.hdmicec.report_active_source.value:
							self.sendMessage(message.getAddress(), 'sourceactive')
			elif cmd == 0x85: # request active source
				if not inStandby:
					if config.hdmicec.report_active_source.value:
						self.sendMessage(message.getAddress(), 'sourceactive')
			elif cmd == 0x8c: # request vendor id
				self.sendMessage(message.getAddress(), 'vendorid')
			elif cmd == 0x8d: # menu request
				requesttype = ord(data[0])
				if requesttype == 2: # query
					if inStandby:
						self.sendMessage(message.getAddress(), 'menuinactive')
					else:
						self.sendMessage(message.getAddress(), 'menuactive')

			# handle standby request from the tv
			if cmd == 0x36 and config.hdmicec.handle_tv_standby.value:
				self.standby()

			# handle wakeup requests from the tv
			if config.hdmicec.handle_tv_wakeup.value:
				if cmd == 0x04 and config.hdmicec.tv_wakeup_detection.value == "wakeup":
					self.wakeup()
				elif cmd == 0x85 and config.hdmicec.tv_wakeup_detection.value == "sourcerequest":
					self.wakeup()
				elif cmd == 0x86 and config.hdmicec.tv_wakeup_detection.value == "streamrequest":
					physicaladdress = ord(data[0]) * 256 + ord(data[1])
					ouraddress = eHdmiCEC.getInstance().getPhysicalAddress()
					if physicaladdress == ouraddress:
						self.wakeup()
				elif cmd == 0x46 and config.hdmicec.tv_wakeup_detection.value == "osdnamerequest":
					self.wakeup()
				elif config.hdmicec.tv_wakeup_detection.value == "activity":
					self.wakeup()

hdmi_cec = HdmiCec()
