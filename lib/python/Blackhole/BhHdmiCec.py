# Module initialized by BlackHoleApi

from Components.config import config, ConfigSelection, ConfigYesNo, ConfigSubsection
from enigma import eHdmiCEC


class HdmiCec:
	def __init__(self):
		config.hdmicec = ConfigSubsection()
		config.hdmicec.tvstandby = ConfigYesNo(default = False)
		config.hdmicec.tvwakeup = ConfigYesNo(default = False)
		config.hdmicec.boxstandby = ConfigYesNo(default = False)
		config.hdmicec.boxwakeup = ConfigYesNo(default = False)
		
		eHdmiCEC.getInstance().messageReceived.get().append(self.messageReceived)
		config.misc.standbyCounter.addNotifier(self.enterStandby, initial_call = False)

	def sendMessages(self, address, messages):
		for message in messages.split(','):
			if message == "active":
				address = 0x0F

			eHdmiCEC.getInstance().sendMessage(address, message)
			print "sent cec message %s to %s" % (message, address)

	def leaveStandby(self):
		if config.hdmicec.boxwakeup.value:
			self.sendMessages(0, "wake,active")

	def enterStandby(self, configElement):
		from Screens.Standby import inStandby
		inStandby.onClose.append(self.leaveStandby)
		if config.hdmicec.boxstandby.value:
			self.sendMessages(0x0F, "sleep")

	def messageReceived(self, address, message):
#		print "received cec message %x from %x" % (message, address)
		if message == 0x85 and config.hdmicec.tvwakeup.value:
			from Screens.Standby import Standby, inStandby
			if inStandby:
				inStandby.Power()
		if message == 0x36 and config.hdmicec.tvstandby:
			from Screens.Standby import Standby, inStandby
			if not inStandby:
				from Tools import Notifications
				Notifications.AddNotification(Standby)
		if message == 0x46:
			self.sendMessages(0, "setname")
		if message == 0x8F:
			self.sendMessages(0, "reportpower")
			
hdmi_cec = HdmiCec()
