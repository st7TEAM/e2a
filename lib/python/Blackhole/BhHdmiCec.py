# Module initialized by BlackHoleApi

from Components.config import config, ConfigSelection, ConfigYesNo, ConfigSubsection, ConfigSelection
from enigma import eHdmiCEC


class HdmiCec:
	def __init__(self):
		config.hdmicec = ConfigSubsection()
		config.hdmicec.on = ConfigYesNo(default = True)
		config.hdmicec.port = ConfigSelection(default = "1", choices = [
		("1", "Vu+ -> Tv Hdmi-1"), ("2", "Vu+ -> Tv Hdmi-2"), ("3", "Vu+ -> Tv Hdmi-3"), ("4", "Vu+ -> Tv Hdmi-4"),
		("5", "Vu+ -> Ampli Hdmi-1 -> Tv Hdmi-1")])
		config.hdmicec.tvstandby = ConfigYesNo(default = False)
		config.hdmicec.tvwakeup = ConfigYesNo(default = False)
		config.hdmicec.boxstandby = ConfigYesNo(default = False)
		
		
		eHdmiCEC.getInstance().messageReceived.get().append(self.messageReceived)
		config.misc.standbyCounter.addNotifier(self.enterStandby, initial_call = False)
		

	def sendMessages(self, address, message):
		eHdmiCEC.getInstance().sendMessage(address, message)

#	def leaveStandby(self):
#		if config.hdmicec.boxwakeup.value:
#			self.sendMessages(0, "wake")

	def enterStandby(self, configElement):
		from Screens.Standby import inStandby
#		inStandby.onClose.append(self.leaveStandby)
		if config.hdmicec.boxstandby.value:
			self.sendMessages(0, 0x36)
			self.sendMessages(0x0F, 0x36)

	def messageReceived(self, address, message):
		if message == 0x85 and config.hdmicec.tvwakeup.value:
			from Screens.Standby import Standby, inStandby
			if inStandby:
				inStandby.Power()
		if message == 0x36 and config.hdmicec.tvstandby:
			from Screens.Standby import Standby, inStandby
			if not inStandby:
				from Tools import Notifications
				Notifications.AddNotification(Standby)
					
hdmi_cec = HdmiCec()
