from Screens.Screen import Screen
from Components.ConfigList import ConfigListScreen
from Components.config import config, getConfigListEntry, ConfigSubsection, ConfigSelection
from Components.ActionMap import ActionMap
from Screens.MessageBox import MessageBox
from Components.Sources.StaticText import StaticText
from Plugins.Plugin import PluginDescriptor
from Tools.Directories import fileExists
from enigma import eTimer

config.plugins.remotecontrolcode = ConfigSubsection()
config.plugins.remotecontrolcode.systemcode = ConfigSelection(default = "2", choices = 
	[ ("1", "1 "), ("2", "2 "), ("3", "3 "), ("4", "4 ") ] )

class RemoteControlCodeInit:
	def __init__(self):
		self.setSystemCode(int(config.plugins.remotecontrolcode.systemcode.value))

	def setSystemCode(self, type = 2):
		if not fileExists("/proc/stb/fp/remote_code"):
			return -1
		print "<RemoteControlCode> Write Remote Control Code : %d" % type
		f = open("/proc/stb/fp/remote_code", "w")
		f.write("%d" % type)
		f.close()
		return 0

	def getModel(self):
		if fileExists("/proc/stb/info/vumodel"):
			vumodel = open("/proc/stb/info/vumodel")
			info=vumodel.read().strip()
			vumodel.close()
			if info in ["uno", "ultimo"]:
				return True
			else:
				return False
		else:
			return False

class RemoteControlCode(Screen,ConfigListScreen,RemoteControlCodeInit):
	skin = """
			<screen name="RemoteControlCode" position="center,center" size="560,300" title="Remote Control System Code Setting" >
			<ePixmap pixmap="Vu_HD/buttons/red.png" position="10,10" size="25,25" alphatest="on" />
			<ePixmap pixmap="Vu_HD/buttons/green.png" position="290,10" size="25,25" alphatest="on" />
			<widget source="key_red" render="Label" position="40,10" zPosition="1" size="140,25" font="Regular;20" halign="center" valign="center" transparent="1" />
			<widget source="key_green" render="Label" position="320,10" zPosition="1" size="140,25" font="Regular;20" halign="center" valign="center" transparent="1" />
			<widget name="config" zPosition="2" position="5,50" size="550,200" scrollbarMode="showOnDemand" transparent="1" />
			</screen>"""

	def __init__(self,session):
		Screen.__init__(self,session)
		self.session = session
		self["shortcuts"] = ActionMap(["ShortcutActions", "SetupActions" ],
		{
			"ok": self.keySave,
			"cancel": self.keyCancel,
			"red": self.keyCancel,
			"green": self.keySave,
		}, -2)
		self.list = []
		ConfigListScreen.__init__(self, self.list,session = self.session)
		self["key_red"] = StaticText(_("Cancel"))
		self["key_green"] = StaticText(_("Save"))
		self.createSetup()
		self.onLayoutFinish.append(self.checkModel)
		self.checkModelTimer = eTimer()
		self.checkModelTimer.callback.append(self.invalidmodel)

	def checkModel(self):
		if not self.getModel():
			self.checkModelTimer.start(1000,True)

	def invalidmodel(self):
			self.session.openWithCallback(self.close, MessageBox, _("This Plugin only support for UNO/ULTIMO"), MessageBox.TYPE_ERROR)

	def createSetup(self):
		self.list = []
		self.rcsctype = getConfigListEntry(_("Remote Control System Code"), config.plugins.remotecontrolcode.systemcode)
		self.list.append( self.rcsctype )
		self["config"].list = self.list
		self["config"].l.setList(self.list)

	def keySave(self):
		print "<RemoteControlCode> Selected System Code : ",config.plugins.remotecontrolcode.systemcode.value
		ret = self.setSystemCode(int(config.plugins.remotecontrolcode.systemcode.value))
		if ret == -1:
			self.restoreCode()
			self.session.openWithCallback(self.close, MessageBox, _("FILE NOT EXIST : /proc/stb/fp/remote_code"), MessageBox.TYPE_ERROR)
		else:
			self.session.openWithCallback(self.MessageBoxConfirmCodeCallback, MessageBoxConfirmCode, _("The remote control code will be reset to previous setting"), MessageBox.TYPE_YESNO, timeout = 10, default = False)

	def restoreCode(self):
		for x in self["config"].list:
			x[1].cancel()

	def MessageBoxConfirmCodeCallback(self,ret):
		if ret:
			ConfigListScreen.keySave(self)
		else:
			self.restoreCode()
			self.setSystemCode(int(config.plugins.remotecontrolcode.systemcode.value))

class MessageBoxConfirmCode(MessageBox):
	skin = """
		<screen position="center,center" size="600,10" title="Message">
		<widget name="text" position="65,8" size="420,0" font="Regular;22" />
		<widget name="ErrorPixmap" pixmap="Vu_HD/icons/input_error.png" position="5,5" size="53,53" alphatest="blend" />
		<widget name="QuestionPixmap" pixmap="Vu_HD/icons/input_question.png" position="5,5" size="53,53" alphatest="blend" />
		<widget name="InfoPixmap" pixmap="Vu_HD/icons/input_info.png" position="5,5" size="53,53" alphatest="blend" />
		<widget name="list" position="100,100" size="380,375" transparent="1" backgroundColor="darkgrey" />
		<applet type="onLayoutFinish">
# this should be factored out into some helper code, but currently demonstrates applets.
from enigma import eSize, ePoint

orgwidth = self.instance.size().width()
orgpos = self.instance.position()
textsize = self[&quot;text&quot;].getSize()

# y size still must be fixed in font stuff...
textsize = (textsize[0] + 50, textsize[1] + 50)
offset = 0
if self.type == self.TYPE_YESNO:
	offset = 60
wsizex = textsize[0] + 60
wsizey = textsize[1] + offset
if (280 &gt; wsizex):
	wsizex = 280
wsize = (wsizex, wsizey)


# resize
self.instance.resize(eSize(*wsize))

# resize label
self[&quot;text&quot;].instance.resize(eSize(*textsize))

# move list
listsize = (wsizex, 50)
self[&quot;list&quot;].instance.move(ePoint(0, textsize[1]))
self[&quot;list&quot;].instance.resize(eSize(*listsize))

# center window
newwidth = wsize[0]
self.instance.move(ePoint(orgpos.x() + (orgwidth - newwidth)/2, orgpos.y()))
		</applet>
	</screen>"""

	def __init__(self, session, text, type = MessageBox.TYPE_YESNO, timeout = -1, close_on_any_key = False, default = True, enable_input = True, msgBoxID = None):
		MessageBox.__init__(self,session,text,type,timeout,close_on_any_key,default,enable_input,msgBoxID)
		if type == MessageBox.TYPE_YESNO:
			self.list = [ (_("Keep"), 0), (_("Restore"), 1) ]
			self["list"].setList(self.list)

	def timerTick(self):
		if self.execing:
			self.timeout -= 1
			self["text"].setText(self.text + " in %d seconds." %self.timeout)
			if self.timeout == 0:
				self.timer.stop()
				self.timerRunning = False
				self.timeoutCallback()

	def move(self, direction):
		if self.close_on_any_key:
			self.close(True)
		self["list"].instance.moveSelection(direction)
		if self.list:
			self["selectedChoice"].setText(self["list"].getCurrent()[0])
#		self.stopTimer()

	def timeoutCallback(self):
		self.close(False)

def main(session, **kwargs):
	session.open(RemoteControlCode)

def Plugins(**kwargs):
	return [PluginDescriptor(name=_("RemoteControlCode"), description="setup Remote Control System Code Type", where = PluginDescriptor.WHERE_PLUGINMENU, needsRestart = True, fnc=main)]

remotecontrolcodeinit = RemoteControlCodeInit()
