from Screens.Screen import Screen

from enigma import eTimer
from Screens.MessageBox import MessageBox
from Screens.Standby import TryQuitMainloop
from Components.ActionMap import ActionMap
from Components.Label import Label
from Components.Pixmap import Pixmap
from Components.ConfigList import ConfigListScreen
from Components.config import getConfigListEntry, config, ConfigYesNo, ConfigText, ConfigSelection, ConfigClock, NoSave, configfile
from Components.Sources.List import List
from Tools.LoadPixmap import LoadPixmap
from Tools.Directories import fileExists, pathExists, createDir, resolveFilename, SCOPE_SKIN_IMAGE
from os import system, remove as os_remove, rename as os_rename, popen, getcwd, chdir
from BhUtils import DeliteGetSkinPath, nab_Detect_Machine, BhU_get_Version
from BhInadyn import DeliteInadyn
from BhSwap import DeliteSwap
from BhHdd import DeliteHdd
from BhNet import DeliteOpenvpn, DeliteSamba, DeliteTelnet, DeliteFtp, BhDjmount, BhMediatomb
from BhNfs import DeliteNfs
from BhMountWiz import DeliteMountWiz

from enigma import eTimer
from Screens.Console import Console
from Screens.VirtualKeyBoard import VirtualKeyBoard

import time
import datetime

class DeliteSettings(Screen):
	skin = """
	<screen position="160,110" size="390,360" title="Black Hole Settings">
		<widget source="list" render="Listbox" position="10,10" size="370,330" scrollbarMode="showOnDemand" >
			<convert type="TemplatedMultiContent">
                		{"template": [
                		MultiContentEntryText(pos = (60, 1), size = (300, 36), flags = RT_HALIGN_LEFT|RT_VALIGN_CENTER, text = 0),
                		MultiContentEntryPixmapAlphaTest(pos = (4, 2), size = (36, 36), png = 1),
                		],
                		"fonts": [gFont("Regular", 24)],
                		"itemHeight": 36
                		}
            		</convert>
		</widget>
	</screen>"""
	
	def __init__(self, session):
		Screen.__init__(self, session)
		
		self.list = []
		self["list"] = List(self.list)
		self.updateList()
		
		
		self["actions"] = ActionMap(["WizardActions", "ColorActions"],
		{
			"ok": self.KeyOk,
			"back": self.close

		})
		
	def KeyOk(self):
		self.sel = self["list"].getCurrent()
		self.sel = self.sel[2]
		
		if self.sel == 0:
			self.session.open(DeliteCronMang)
		elif self.sel == 1:
			self.session.open(DeliteSetupOSD2)
		elif self.sel == 2:
			self.session.open(DeliteDevicesPanel)
		elif self.sel == 3:
			self.session.open(BhHdmiCecConf)
		elif self.sel == 4:
			self.session.open(DeliteKernelModules)
		elif self.sel == 5:
			self.session.open(DeliteInadyn)
		elif self.sel == 6:
			self.session.open(DeliteSwap)
		elif self.sel == 7:
			self.session.open(DeliteHdd)
		elif self.sel == 8:
			self.session.open(DeliteMountWiz)
		elif self.sel == 9:
			self.session.open(DeliteOpenvpn)
		elif self.sel == 10:
			self.session.open(DeliteSamba)
		elif self.sel == 11:
			self.session.open(DeliteNfs)
		elif self.sel == 12:
			self.session.open(DeliteTelnet)
		elif self.sel == 13:
			self.session.open(DeliteFtp)
		elif self.sel == 14:
			self.session.open(DeliteDtt)
		elif self.sel == 15:
			self.session.open(BhDjmount)
		elif self.sel == 16:
			self.session.open(BhMediatomb)
		else:
			self.noYet()
		
	def noYet(self):
		nobox = self.session.open(MessageBox, "Function Not Yet Available", MessageBox.TYPE_INFO)
		nobox.setTitle(_("Info"))
	
		
	def updateList(self):
		self.list = [ ]
		mypath = DeliteGetSkinPath()
		
		mypixmap = mypath + "icons/infopanel_cron.png"
		png = LoadPixmap(mypixmap)
		name = "Black Hole Cron Manager"
		idx = 0
		res = (name, png, idx)
		self.list.append(res)
		
		
		mypixmap = mypath + "icons/infopanel_osd.png"
		png = LoadPixmap(mypixmap)
		name = "Osd Settings"
		idx = 1
		res = (name, png, idx)
		self.list.append(res)
		
		mypixmap = mypath + "icons/infopanel_space.png"
		png = LoadPixmap(mypixmap)
		name = "Devices Manager"
		idx = 2
		res = (name, png, idx)
		self.list.append(res)
		
		mypixmap = mypath + "icons/infopanel_samba.png"
		png = LoadPixmap(mypixmap)
		name = "Black Hole Hdmi Cec"
		idx = 3
		res = (name, png, idx)
		self.list.append(res)
		
		mypixmap = mypath + "icons/infopanel_kmod.png"
		png = LoadPixmap(mypixmap)
		name = "Kernel Modules Manager"
		idx = 4
		res = (name, png, idx)
		self.list.append(res)
		
		mypixmap = mypath + "icons/inadynsettings.png"
		png = LoadPixmap(mypixmap)
		name = "Inadyn Settings"
		idx = 5
		res = (name, png, idx)
		self.list.append(res)
		
		mypixmap = mypath + "icons/swapsettings.png"
		png = LoadPixmap(mypixmap)
		name = "Swap File Settings"
		idx = 6
		res = (name, png, idx)
		self.list.append(res)
		
		mypixmap = mypath + "icons/hdsettings.png"
		png = LoadPixmap(mypixmap)
		name = "Hard Disk Settings"
		idx = 7
		res = (name, png, idx)
		self.list.append(res)
		
		mypixmap = mypath + "icons/mountwizard.png"
		png = LoadPixmap(mypixmap)
		name = "Black Hole Mount Wizard"
		idx = 8
		res = (name, png, idx)
		self.list.append(res)
		
		mypixmap = mypath + "icons/infopanel_vpn.png"
		png = LoadPixmap(mypixmap)
		name = "OpenVpn Panel"
		idx = 9
		res = (name, png, idx)
		self.list.append(res)
		
		mypixmap = mypath + "icons/infopanel_samba.png"
		png = LoadPixmap(mypixmap)
		name = "Samba/Cifs Panel"
		idx = 10
		res = (name, png, idx)
		self.list.append(res)
		
		mypixmap = mypath + "icons/infopanel_nfs.png"
		png = LoadPixmap(mypixmap)
		name = "Nfs Server Panel"
		idx = 11
		res = (name, png, idx)
		self.list.append(res)
		
		mypixmap = mypath + "icons/infopanel_telnet.png"
		png = LoadPixmap(mypixmap)
		name = "Telnet Panel"
		idx = 12
		res = (name, png, idx)
		self.list.append(res)
		
		mypixmap = mypath + "icons/infopanel_ftp.png"
		png = LoadPixmap(mypixmap)
		name = "Ftp Panel"
		idx = 13
		res = (name, png, idx)
		self.list.append(res)
		
		mypixmap = mypath + "icons/infopanel_space.png"
		png = LoadPixmap(mypixmap)
		name = "Usb Tuner Panel"
		idx = 14
		res = (name, png, idx)
		self.list.append(res)
		
		mypixmap = mypath + "icons/infopanel_samba.png"
		png = LoadPixmap(mypixmap)
		name = "UPnP Client Djmount"
		idx = 15
		res = (name, png, idx)
		self.list.append(res)
		
		mypixmap = mypath + "icons/infopanel_samba.png"
		png = LoadPixmap(mypixmap)
		name = "UPnP Server Mediatomb"
		idx = 16
		res = (name, png, idx)
		self.list.append(res)
		
		self["list"].list = self.list
		


#DeliteSetupOSD
class DeliteSetupOSD2(Screen):
	skin = """
	<screen position="339,190" size="602,340" title="Black Hole Osd Settings">
		<widget name="lsinactive" position="10,20" zPosition="1" pixmap="skin_default/icons/ninactive.png" size="32,32" alphatest="on"/>
		<widget name="lsactive" position="10,20" zPosition="2" pixmap="skin_default/icons/nactive.png" size="32,32" alphatest="on"/>
		<widget name="lab1" position="50,20" size="260,30" font="Regular;20" valign="center" transparent="1"/>
		<widget name="lbinactive" position="10,70" zPosition="1" pixmap="skin_default/icons/ninactive.png" size="32,32" alphatest="on"/>
		<widget name="lbactive" position="10,70" zPosition="2" pixmap="skin_default/icons/nactive.png" size="32,32" alphatest="on"/>
		<widget name="lab4" position="50,70" size="550,50" font="Regular;20" valign="center" transparent="1"/>
		<widget name="lpinactive" position="10,130" zPosition="1" pixmap="skin_default/icons/ninactive.png" size="32,32" alphatest="on"/>
		<widget name="lpactive" position="10,130" zPosition="2" pixmap="skin_default/icons/nactive.png" size="32,32" alphatest="on"/>
		<widget name="lab2" position="50,130" size="260,30" font="Regular;20" valign="center" transparent="1"/>
		<widget name="lab3" position="10,180" size="320,30" font="Regular;20" valign="center" transparent="1"/>
		<widget name="labsize" position="330,180" size="30,30" font="Regular;20" valign="center" backgroundColor="#4D5375"/>
		<ePixmap pixmap="skin_default/buttons/red.png" position="235,290" size="150,40" alphatest="on"/>
		<widget name="key_red" position="235,290" zPosition="1" size="150,40" font="Regular;18" halign="center" valign="center" backgroundColor="#9f1313" transparent="1"/>
	</screen>"""
	
	def __init__(self, session):
		Screen.__init__(self, session)
		
		
		self["lab1"] = Label(_("Disable Light Skin on Zap"))
		self["lsinactive"] = Pixmap()
		self["lsactive"] = Pixmap()
		
		self["lbinactive"] = Pixmap()
		self["lbactive"] = Pixmap()
		self["lab4"] = Label(_("Enable Panic button 0 (zap to 1 & clear zap history)"))
		
		self["lab2"] = Label(_("Enable LCD Picons"))
		self["lpinactive"] = Pixmap()
		self["lpactive"] = Pixmap()
		self["lab3"] = Label(_("Hide Infobar Timeout in sec.:"))
		self["labsize"] = Label("")
		
		self["key_red"] = Label(_("Setup"))
		
		self["actions"] = ActionMap(["WizardActions", "ColorActions"],
		{
			"back": self.close,
			"red": self.setupmyosd
		})
		
		lab2txt = "Enable LCD Picons"
		machine = nab_Detect_Machine()
		if machine == "et9000":
			lab2txt = "unused in " + machine
		elif machine == "dm500hd":
			lab2txt = "unused in " + machine
		elif machine == "bm750":
			lab2txt = "unused in Vu Duo"
		elif machine == "vusolo":
			lab2txt = "unused in Vu Solo"	
				
		self["lab2"].setText(lab2txt)
		
		self.onLayoutFinish.append(self.updatemyinfo)
		
	def updatemyinfo(self):
		
		self["lsinactive"].hide()
		self["lsactive"].hide()
		self["lpinactive"].hide()
		self["lpactive"].hide()
		self["lbinactive"].hide()
		self["lbactive"].hide()
		
		if config.misc.deliteeinfo.value:
			self["lsactive"].show()
		else:
			self["lsinactive"].show()
		
		if config.misc.delitepiconlcd.value:
			self["lpactive"].show()
		else:
			self["lpinactive"].show()
			
		if config.misc.delitepanicb.value:
			self["lbactive"].show()
		else:
			self["lbinactive"].show()
			
		myt = "5"
		idx = config.usage.infobar_timeout.index
		if idx:
			myt = str(idx)
				
		self["labsize"].setText(myt)
		
		
	def setupmyosd(self):
		self.session.openWithCallback(self.updatemyinfo, DeliteSetupOSDConf2)

#DeliteSetupOSDConf			
class DeliteSetupOSDConf2(Screen, ConfigListScreen):
	skin = """
	<screen position="339,190" size="602,340" title="Black Hole OSD Setup">
		<widget name="config" position="10,10" size="580,200" scrollbarMode="showOnDemand"/>
		<ePixmap pixmap="skin_default/buttons/red.png" position="235,290" size="150,40" alphatest="on"/>
		<widget name="key_red" position="235,290" zPosition="1" size="150,40" font="Regular;20" halign="center" valign="center" backgroundColor="#9f1313" transparent="1"/>
	</screen>"""
	
	def __init__(self, session):
		Screen.__init__(self, session)
		
		self.list = []
		ConfigListScreen.__init__(self, self.list)
		self["key_red"] = Label(_("Save"))
		
		
		self["actions"] = ActionMap(["WizardActions", "ColorActions"],
		{
			"red": self.saveMyosd,
			"back": self.close

		})
			
		self.updateList()
	
	
	def updateList(self):
	
		self.deliteeinfo = NoSave(ConfigYesNo(default="False"))
		self.delitepanicb = NoSave(ConfigYesNo(default="False"))
		self.delitepiconlcd = NoSave(ConfigYesNo(default="False"))
		self.infobar_timeout = NoSave(ConfigSelection(default = "5", choices = [
		("0", _("no timeout")), ("1", "1 " + _("second")), ("2", "2 " + _("seconds")), ("3", "3 " + _("seconds")),
		("4", "4 " + _("seconds")), ("5", "5 " + _("seconds")), ("6", "6 " + _("seconds")), ("7", "7 " + _("seconds")),
		("8", "8 " + _("seconds")), ("9", "9 " + _("seconds")), ("10", "10 " + _("seconds"))]))
		
		self.plcd_original = config.misc.delitepiconlcd.value
		
		self.deliteeinfo.value = config.misc.deliteeinfo.value
		self.delitepanicb.value = config.misc.delitepanicb.value
		self.delitepiconlcd.value = config.misc.delitepiconlcd.value
		self.infobar_timeout.value = config.usage.infobar_timeout.value
		
		lab2txt = "Enable LCD Picons"
		machine = nab_Detect_Machine()
		if machine == "et9000":
			lab2txt = "unused in " + machine
		elif machine == "dm500hd":
			lab2txt = "unused in " + machine
		elif machine == "bm750":
			lab2txt = "unused in Vu Duo"
		elif machine == "vusolo":
			lab2txt = "unused in Vu Solo"
		
		osd_ei = getConfigListEntry(_("Disable Light Skin on Zap"), self.deliteeinfo)
		self.list.append(osd_ei)
		
		osd_panic = getConfigListEntry(_("Enable Panic button 0"), self.delitepanicb)
		self.list.append(osd_panic)
		
		osd_lcdpicon = getConfigListEntry(lab2txt, self.delitepiconlcd)
		self.list.append(osd_lcdpicon)
		
		infobar_timeout = getConfigListEntry(_("Hide Infobar Timeout in sec."), self.infobar_timeout)
		self.list.append(infobar_timeout)
		
		self["config"].list = self.list
		self["config"].l.setList(self.list)
		
		
	def saveMyosd(self):
		
		config.misc.deliteeinfo.value = self.deliteeinfo.value
		config.misc.delitepanicb.value = self.delitepanicb.value
		config.misc.delitepiconlcd.value = self.delitepiconlcd.value
		config.usage.infobar_timeout.value = self.infobar_timeout.value
		
		config.misc.deliteeinfo.save()
		config.misc.delitepanicb.save()
		
		machine = nab_Detect_Machine()
		good = ["dm8000", "dm800", "dm800se", "dm7020hd"]
		if machine in good:
			config.misc.delitepiconlcd.save()
		
		config.usage.infobar_timeout.save()
		
		if self.plcd_original != self.delitepiconlcd.value:
			message = "Picons LCD changes need gui restart to take effects.\nRestart Gui now?"
			ybox = self.session.openWithCallback(self.restEn, MessageBox, message, MessageBox.TYPE_YESNO)
			ybox.setTitle("Gui Restart.")
		else:
			self.close()
			
	def restEn(self, answer):
		if answer is True:
			self.session.open(TryQuitMainloop, 3)
		else:
			self.close()



class DeliteCronMang(Screen):
	skin = """
	<screen position="240,120" size="800,520" title="Black Hole Cron Manager">
		<widget source="list" render="Listbox" position="10,10" size="780,460" scrollbarMode="showOnDemand" >
			<convert type="StringList" />
		</widget>
    		<ePixmap pixmap="skin_default/buttons/red.png" position="200,480" size="140,40" alphatest="on" />
		<ePixmap pixmap="skin_default/buttons/yellow.png" position="440,480" size="140,40" alphatest="on" />
		<widget name="key_red" position="200,480" zPosition="1" size="140,40" font="Regular;20" halign="center" valign="center" backgroundColor="#9f1313" transparent="1" />
		<widget name="key_yellow" position="440,480" zPosition="1" size="140,40" font="Regular;20" halign="center" valign="center" backgroundColor="#a08500" transparent="1" />
    	</screen>"""
	
	def __init__(self, session):
		Screen.__init__(self, session)
		
		self["key_red"] = Label(_("Add"))
		self["key_yellow"] = Label(_("Delete"))
		
		self.list = []
		self["list"] = List(self.list)
		
		self["actions"] = ActionMap(["WizardActions", "ColorActions"],
		{
			"ok": self.close,
			"back": self.close,
			"red": self.addtocron,
			"yellow": self.delcron
		})
		
		self.updateList()
		
	def addtocron(self):
		self.session.openWithCallback(self.updateList, DeliteSetupCronConf)
		
	def updateList(self):
		self.list = [ ]
		if fileExists("/etc/bhcron/root"):
			f = open("/etc/bhcron/root",'r')
			for line in f.readlines():
				parts = line.strip().split()
				line2 = "Time: " + parts[1] + ":" + parts[0] + "\t" + "Command: " + line[(line.rfind('*') +1):]			
				res = (line2, line)
				self.list.append(res)
			f.close()

		self["list"].list = self.list

	def delcron(self):
		mysel = self["list"].getCurrent()
		if mysel:
			myline = mysel[1]
			out = open("/etc/bhcron/bh.cron", "w")
			f = open("/etc/bhcron/root",'r')
			for line in f.readlines():
				if line != myline:
					out.write(line)
			f.close()
			out.close()
			rc = system("crontab /etc/bhcron/bh.cron -c /etc/bhcron/")
			self.updateList()


class DeliteSetupCronConf(Screen, ConfigListScreen):
	skin = """
	<screen position="240,190" size="800,340" title="Black Hole Cron Setup">
		<widget name="config" position="10,20" size="780,280" scrollbarMode="showOnDemand" />
		<ePixmap pixmap="skin_default/buttons/red.png" position="330,270" size="140,40" alphatest="on" />
		<widget name="key_red" position="330,270" zPosition="1" size="140,40" font="Regular;20" halign="center" valign="center" backgroundColor="#9f1313" transparent="1" />
	</screen>"""
	
	def __init__(self, session):
		Screen.__init__(self, session)
		
		self.list = []
		ConfigListScreen.__init__(self, self.list)
		self["key_red"] = Label(_("Save"))
		
		self["actions"] = ActionMap(["WizardActions", "ColorActions"],
		{
			"red": self.checkentry,
			"back": self.close,
			"green": self.vkeyb

		})
		self.updateList()
	
			
	def updateList(self):
	
		self.cmdtime = NoSave(ConfigClock(default=0))
		self.default_command = NoSave(ConfigSelection(default = "None", choices = [
		("None", "None"), ("/usr/bin/Blackholecmd standby", "standby"), ("/usr/bin/Blackholecmd shutdown", "shutdown"), ("/usr/bin/Blackholecmd reboot", "reboot"),
		("/usr/bin/Blackholecmd restartenigma2", "restartgui"), ("/usr/bin/Blackholecmd restartemu", "restartemu")]))
		self.user_command = NoSave(ConfigText(fixed_size = False))
		self.cmdtime.value = mytmpt = [0,0]
		self.default_command.value = "None"
		self.user_command.value = "None"
		
		res = getConfigListEntry("Time to execute command or script", self.cmdtime)
		self.list.append(res)
		res = getConfigListEntry("Predefined Command to execute", self.default_command)
		self.list.append(res)
		res = getConfigListEntry("Custom Command", self.user_command)
		self.list.append(res)
		
		self["config"].list = self.list
		self["config"].l.setList(self.list)
	
	
	def vkeyb(self):
		sel = self["config"].getCurrent()
		if sel:
			self.vkvar = sel[0]
			value = "xmeo"
			if self.vkvar == "Custom Command":
				value = self.user_command.value
				if value == "None":
					value = ""
			
			if value != "xmeo":
				self.session.openWithCallback(self.UpdateAgain, VirtualKeyBoard, title=self.vkvar, text=value)
			else:
				self.session.open(MessageBox, "Please use Virtual Keyboard for text rows only (e.g. Custom Command)", MessageBox.TYPE_INFO)
	
	def UpdateAgain(self, newt):
		self.list = [ ]
		if newt is None or newt == "":
			newt = "None"
		self.user_command.value = newt
		
		res = getConfigListEntry("Time to execute command or script", self.cmdtime)
		self.list.append(res)
		res = getConfigListEntry("Predefined Command to execute", self.default_command)
		self.list.append(res)
		res = getConfigListEntry("Custom Command", self.user_command)
		self.list.append(res)
		
		self["config"].list = self.list
		self["config"].l.setList(self.list)
		#self.session.open(MessageBox, "aggiornata", MessageBox.TYPE_INFO)	
	
	
	def checkentry(self):
		msg = ""
		if self.user_command.value == "None":
			self.user_command.value = ""
		if self.default_command.value == "None" and self.user_command.value == "":
			msg = "You must set at least one Command"
		if self.default_command.value != "None" and self.user_command.value != "":
			msg = "Entering a Custom command you have to set Predefined command: None "

		if msg:
			self.session.open(MessageBox, msg, MessageBox.TYPE_ERROR)
		else:
			self.saveMycron()
			
	def saveMycron(self):
		hour = "%02d" % (self.cmdtime.value[0])
		minutes =  "%02d" % (self.cmdtime.value[1])
		if self.default_command.value != "None":
			command = self.default_command.value
		else:
			command = self.user_command.value
		newcron = minutes + " " + hour + " * * * " + command.strip() + "\n"
		
		out = open("/etc/bhcron/bh.cron", "w")
		if fileExists("/etc/bhcron/root"):
			f = open("/etc/bhcron/root",'r')
			for line in f.readlines():
				out.write(line)
			f.close()
		out.write(newcron)
		out.close()
		rc = system("crontab /etc/bhcron/bh.cron -c /etc/bhcron/")
		self.close()
		
		
class DeliteDevicesPanel(Screen):
	skin = """
	<screen position="240,100" size="800,560" title="Black Hole Devices Manager">
		<widget source="list" render="Listbox" position="10,0" size="780,510" scrollbarMode="showOnDemand" >
			<convert type="TemplatedMultiContent">
                	{"template": [
              		 MultiContentEntryText(pos = (90, 0), size = (690, 30), font=0, text = 0),
               		 MultiContentEntryText(pos = (110, 30), size = (670, 50), font=1, flags = RT_VALIGN_TOP, text = 1),
               		 MultiContentEntryPixmapAlphaTest(pos = (0, 0), size = (80, 80), png = 2),
                	],
                	"fonts": [gFont("Regular", 24),gFont("Regular", 20)],
                	"itemHeight": 85
                	}
            		</convert>
		</widget>
		<widget name="lab1" zPosition="2" position="50,40" size="700,40" font="Regular;24" halign="center" transparent="1"/>
    		<ePixmap pixmap="skin_default/buttons/red.png" position="200,524" size="140,40" alphatest="on" />
		<ePixmap pixmap="skin_default/buttons/yellow.png" position="440,524" size="140,40" alphatest="on" />
		<widget name="key_red" position="200,520" zPosition="1" size="200,40" font="Regular;20" halign="center" valign="center" backgroundColor="#9f1313" transparent="1" />
		<widget name="key_yellow" position="440,520" zPosition="1" size="140,40" font="Regular;20" halign="center" valign="center" backgroundColor="#a08500" transparent="1" />
    	</screen>"""
	
	def __init__(self, session):
		Screen.__init__(self, session)
		
		self["key_red"] = Label(_("Mountpoints"))
		self["key_yellow"] = Label(_("Format"))
		self["lab1"] = Label("Wait please while scanning your devices...")
		
		self.list = []
		self["list"] = List(self.list)
		
		self["actions"] = ActionMap(["WizardActions", "ColorActions"],
		{
			"back": self.close,
			"red": self.mountUmount,
			"yellow": self.myFormat
		})
		
		self.activityTimer = eTimer()
		self.activityTimer.timeout.get().append(self.updateList2)
		self.updateList()
	
	def updateList(self):
		self.activityTimer.start(10)
		
	def updateList2(self):
		self.activityTimer.stop()
		self.list = [ ]
		list2 = [ ]
		system("df > /tmp/ninfo.tmp")
		system ("ls -l /dev/disk/by-uuid/ > /tmp/ninfo2")
		f = open("/tmp/ninfo2",'r')
		for line in f.readlines():
			parts = line.strip().split()
			uid = parts[8]
			device = parts[10]
			device = device.strip().replace('../../', '')
			if device in list2:
				continue
			if device.find("1") == -1:
				continue
			self.buildMy_rec(device, uid)
			list2.append(device)
		f.close()
				
#If not part1		
		f = open("/tmp/ninfo2",'r')
		for line in f.readlines():
			parts = line.strip().split()
			uid = parts[8]
			device = parts[10]
			device = device.strip().replace('../../', '')
			if device.find("1") == -1:
				tempdevice = device + "1"
				if tempdevice in list2:
					continue
				if device in list2:
					continue
				self.buildMy_rec(device, uid)
				list2.append(device)
		f.close()	
	
	
		self["list"].list = self.list
		self["lab1"].hide()
		
	def buildMy_rec(self, device, uid):
		mypath = DeliteGetSkinPath()
		device2 = device.replace('1', '')
		cmd = "udevinfo -a -p /sys/block/" + device2 + " > /tmp/ninfo3.tmp"
		system(cmd)
		name = "USB: "
		mypixmap = mypath + "icons/dev_usb.png"
		des = ""
		f = open("/tmp/ninfo3.tmp",'r')
		for line in f.readlines():
			line = line.strip()
			if line.find("/devices/pci") != -1:
				name = "HARD DISK: "
				mypixmap = mypath + "icons/dev_hdd.png"
			if line.find("{size}") != -1:
				cap = line.replace('ATTR{size}==', '')
				cap = cap[1:-1]
				cap = int(cap)
				cap = cap / 1000 * 512 / 1000
				cap = "%d.%03d GB" % (cap/1000, cap%1000)
				des = "Size: " + cap
			if line.find("{model}") != -1:
				name2 = line.replace('ATTRS{model}==', '')
				name2 = name2[1:-1]
				if name2.find("USB CF Reader") != -1:
					name = "COMPACT FLASH: "
					mypixmap = mypath + "icons/dev_cf.png"
				elif name2.find("USB SD Reader") != -1:
					name = "SD CARD: "
					mypixmap = mypath + "icons/dev_sd.png"
				name = name + name2
				break
			
		f.close()
		d1 = "NOT MAPPED"
		d2 = device
		f = open("/proc/mounts",'r')
		for line in f.readlines():
			if line.find(uid) != -1:
				parts = line.strip().split()
				d1 = parts[1]
				break
		f.close()
		
		if des != "":
			des += "\tMount: " + d1 + "\nDevice: " + "/dev/" + device
			png = LoadPixmap(mypixmap)
			res = (name, des, png)
			self.list.append(res)
		

	def mountUmount(self):
		self.session.openWithCallback(self.updateList, DeliteSetupDevicePanelConf)
					
	def myFormat(self):
		sel = self["list"].getCurrent()
		if sel:
			name = sel[0]
			des = sel[1]
			if des.find('Not Found') != -1:
				self.session.open(MessageBox, des, MessageBox.TYPE_INFO)
				return
			if name.find('DVD DRIVE') != -1:
				self.session.open(MessageBox, "You cannot format DVD drive.", MessageBox.TYPE_INFO)
				return
			if name.find('HARD DISK') != -1:
				self.session.open(MessageBox, "You cannot format HDD with this tool.\nPlease use Hdd manager in Main Menu", MessageBox.TYPE_INFO)
				return
			
			des = des.replace('\n', '\t')
			parts = des.strip().split('\t')
			mountp = parts[1].replace('Mount: ', '')
			device = parts[2].replace('Device: ', '')
			
			self.nformat = name
			self.mformat = mountp
			self.dformat = device
			mess = "Warning you are going to format " + name + "\nALL THE DATA ON THIS DEVICE WILL BE LOST!\n Are you sure to continue?"
			self.session.openWithCallback(self.myFormatDo, MessageBox, mess, MessageBox.TYPE_YESNO)
				
	def myFormatDo(self, answer):
		if answer is True:
			target = self.mformat
			device = self.dformat.replace('1', '')
			
			check = system("killall automount")
			
			if target != "NOT MAPPED":
				cmd = "umount " + target
				check = system(cmd)
			cmd = "umount " + self.dformat
			check = system(cmd)
			
			check = system("umount /dev/sda")
			check = system("umount /dev/sda1")
			check = system("umount /dev/sdb")
			check = system("umount /dev/sdb1")
			check = system("umount /dev/sdc")
			check = system("umount /dev/sdc1")
			check = system("umount /dev/sdd")
			check = system("umount /dev/sdd1")
			check = system("umount /dev/sde")
			check = system("umount /dev/sde1")
			
			
			mycmd = "echo -e '------------------------------------\nPartitioning: " + self.nformat +  "\n------------------------------------\n\n\n ' "
			mycmd1 = 'dd bs=512 count=3 if=/dev/zero of=' + device + "1"
			mycmd2 = 'printf "0,\n;\n;\n;\ny\n" | sfdisk -f ' + device
			self.session.open(Console, title="Partitioning...", cmdlist=[mycmd, mycmd1, mycmd2], finishedCallback = self.myFormatDo2)
			
	def myFormatDo2(self):
		target = self.mformat
		device = self.dformat.replace('1', '')
		
		mycmd = "echo -e '------------------------------------\nFormatting: " + self.nformat +  "\n------------------------------------\n\n\n ' "
#		mycmd1 = "/bin/umount -a"
		mycmd2 = "/sbin/mkfs.ext3 " + device + "1"
		self.session.open(Console, title="Formatting...", cmdlist=[mycmd, mycmd2], finishedCallback = self.updateuuid)
	
	
	def updateuuid(self):
		mybox = self.session.openWithCallback(self.hreBoot, MessageBox, "The Box will be now restarted to generate new device UID.\nDon't forget to remap your device after the reboot.\nPress ok to continue", MessageBox.TYPE_INFO)	
			
	def hreBoot(self, answer):
		self.session.open(TryQuitMainloop, 2)
			
class DeliteSetupDevicePanelConf(Screen, ConfigListScreen):
	skin = """
	<screen position="center,center" size="902,340" title="Black Hole Devices Mountpoints Setup">
		<widget name="config" position="30,10" size="840,275" scrollbarMode="showOnDemand"/>
		<widget name="Linconn" position="30,285" size="840,20" font="Regular;18" halign="center" valign="center" backgroundColor="#9f1313"/>
		<ePixmap pixmap="skin_default/buttons/red.png" position="200,300" size="140,40" alphatest="on"/>
		<ePixmap pixmap="skin_default/buttons/green.png" position="550,300" size="140,40" alphatest="on"/>
		<widget name="key_red" position="200,300" zPosition="1" size="140,40" font="Regular;20" halign="center" valign="center" backgroundColor="#9f1313" transparent="1"/>
		<widget name="key_green" position="550,300" zPosition="1" size="140,40" font="Regular;20" halign="center" valign="center" backgroundColor="#1f771f" transparent="1"/>
	</screen>"""


	def __init__(self, session):
		Screen.__init__(self, session)
		
		self.list = []
		ConfigListScreen.__init__(self, self.list)
		self["key_red"] = Label(_("Save"))
		self["key_green"] = Label(_("Cancel"))
		self["Linconn"] = Label("Wait please while scanning your box devices...")
		
		self["actions"] = ActionMap(["WizardActions", "ColorActions"],
		{
			"red": self.saveMypoints,
			"green": self.close,
			"back": self.close

		})
			
		self.updateList()
	
	
	def updateList(self):
		self.list = []
		list2 = [ ]
		system("df > /tmp/ninfo.tmp")
		system ("ls -l /dev/disk/by-uuid/ > /tmp/ninfo2")
		f = open("/tmp/ninfo2",'r')
		for line in f.readlines():
			parts = line.strip().split()
			uid = parts[8]
			device = parts[10]
			device = device.strip().replace('../../', '')
			if device in list2:
				continue
			if device.find("1") == -1:
				continue
			self.buildMy_rec(device, uid)
			list2.append(device)
		f.close()
		
#If not part1		
		f = open("/tmp/ninfo2",'r')
		for line in f.readlines():
			parts = line.strip().split()
			uid = parts[8]
			device = parts[10]
			device = device.strip().replace('../../', '')
			if device.find("1") == -1:
				tempdevice = device + "1"
				if tempdevice in list2:
					continue
				if device in list2:
					continue
				self.buildMy_rec(device, uid)
				list2.append(device)
		f.close()
		
		
		
		self["config"].list = self.list
		self["config"].l.setList(self.list)
		self["Linconn"].hide()
			
			
	def buildMy_rec(self, device, uid):
		uid = uid.strip()
		device2 = device.replace('1', '')
		cmd = "udevinfo -a -p /sys/block/" + device2 + " > /tmp/ninfo3.tmp"
		system(cmd)
		name = "USB: "
		des = ""
		f = open("/tmp/ninfo3.tmp",'r')
		for line in f.readlines():
			line = line.strip()
			if line.find("/devices/pci") != -1:
				name = "HARD DISK: "
			if line.find("{size}") != -1:
				cap = line.replace('ATTR{size}==', '')
				cap = cap[1:-1]
				cap = int(cap)
				cap = cap / 1000 * 512 / 1000
				cap = "%d.%03d GB" % (cap/1000, cap%1000)
				des = " " + cap
			if line.find("{model}") != -1:
				name2 = line.replace('ATTRS{model}==', '')
				name2 = name2[1:-1]
				if name2.find("USB CF Reader") != -1:
					name = "COMPACT FLASH: "
				elif name2.find("USB SD Reader") != -1:
					name = "SD CARD: "
				name = name + name2.strip()
				break
			
		f.close()
		d1 = "Not mapped"
		checkmb = False
		f = open("/proc/mounts",'r')
		for line in f.readlines():
			if line.find(uid) != -1:
				parts = line.strip().split()
				d1 = parts[1]
				break
			if line.find(device) != -1:
				if line.find("/media/meoboot") != -1:
					d1 = "/media/meoboot"
					break
		f.close()
		
		item = NoSave(ConfigSelection(default = "Not mapped", choices = [
		("Not mapped", "Not mapped"), ("/media/hdd", "/media/hdd"), ("/media/cf", "/media/cf"),
		("/media/card", "/media/card"), ("/media/usb", "/media/usb"), ("/media/usb2", "/media/usb2"), 
		("/media/usb3", "/media/usb3")]))
		
		if d1 == "/media/meoboot":
			item = NoSave(ConfigSelection(default = "/media/meoboot", choices = [("/media/meoboot", "/media/meoboot")]))
		
		item.value = d1.strip()
		text = name + " " + des + " /dev/" + device
		res = getConfigListEntry(text, item, uid)
		if des != "":
			self.list.append(res)
			
	def saveMypoints(self):
		mycheck = False
		
		out = open("/etc/fstab.tmp", "w")
		f = open("/etc/fstab",'r')
		for line in f.readlines():
			if line.find("/dev/sda1") != -1:
				if line.find("#") == -1:
					line = "#" + line
			out.write(line)
		f.close()
		out.close()
		
		mycheck = False
		out = open("/usr/bin/bhmount.tmp",'w')
		for x in self["config"].list:
			uid = x[2]
			mountp = x[1].value
			if mountp == "/media/meoboot":
				continue
			line = "mount /dev/disk/by-uuid/" + uid + " " + mountp + "\n"
			out.write(line)
			if mountp == "Not mapped":
				mycheck = True
		
		out.write('exit 0\n')
		out.close()
		
		if mycheck == True:
			nobox = self.session.open(MessageBox, "Error: You have to set Mountpoins for all your devices.", MessageBox.TYPE_INFO)
			nobox.setTitle(_("Error"))
		else:
			os_rename("/etc/fstab.tmp", "/etc/fstab")
			os_rename("/usr/bin/bhmount.tmp", "/usr/bin/bhmount")
			system("chmod 0755 /usr/bin/bhmount")
			message = "Devices changes need a system restart to take effects.\nRestart your Box now?"
			ybox = self.session.openWithCallback(self.restBo, MessageBox, message, MessageBox.TYPE_YESNO)
			ybox.setTitle("Restart box.")
			
	def restBo(self, answer):
		if answer is True:
			self.session.open(TryQuitMainloop, 2)
		else:
			self.close()

class DeliteKernelModules(Screen, ConfigListScreen):
	skin = """
	<screen position="240,190" size="800,340" title="Black Hole Extra Kernel Modules Setup">
		<widget name="config" position="10,20" size="780,280" scrollbarMode="showOnDemand" />
		<ePixmap pixmap="skin_default/buttons/red.png" position="200,293" size="140,40" alphatest="on" />
		<ePixmap pixmap="skin_default/buttons/yellow.png" position="440,293" size="140,40" alphatest="on" />
		<widget name="key_red" position="200,290" zPosition="1" size="140,40" font="Regular;20" halign="center" valign="center" backgroundColor="#9f1313" transparent="1" />
		<widget name="key_yellow" position="446,290" zPosition="1" size="200,40" font="Regular;20" halign="center" valign="center" backgroundColor="#a08500" transparent="1" />
	
	</screen>"""
	
	def __init__(self, session):
		Screen.__init__(self, session)
		
		self.list = []
		ConfigListScreen.__init__(self, self.list)
		self["key_red"] = Label("Save")
		self["key_yellow"] = Label("Active Modules")
		
		
		self["actions"] = ActionMap(["WizardActions", "ColorActions"],
		{
			"red": self.saveMyconf,
			"yellow": self.showMod,
			"back": self.close

		})
			
		self.updateList()
	
	def showMod(self):
		self.session.open(DeliteKernelModShow)
	
	def updateList(self):
	
		self.ntfs = NoSave(ConfigYesNo(default=False))
		self.ftdi_sio = NoSave(ConfigYesNo(default=False))
		self.pl2303 = NoSave(ConfigYesNo(default=False))
		self.tun = NoSave(ConfigYesNo(default=False))
		self.exportfs = NoSave(ConfigYesNo(default=False))
		self.nfsd = NoSave(ConfigYesNo(default=False))
		
		if fileExists("/usr/bin/bhextramod"):
			f = open("/usr/bin/bhextramod",'r')
			for line in f.readlines():
				if line.find('ntfs') != -1:
					self.ntfs.value = True
				elif line.find('ftdi_sio') != -1:
					self.ftdi_sio.value = True
				elif line.find('pl2303') != -1:
					self.pl2303.value = True
				elif line.find('tun') != -1:
					self.tun.value = True
				elif line.find('exportfs') != -1:
					self.exportfs.value = True
				elif line.find('nfsd') != -1:
					self.nfsd.value = True
			f.close()
		
		res = getConfigListEntry(_("Ntfs for Windows filesystems compatibility:"), self.ntfs)
		self.list.append(res)
		res = getConfigListEntry(_("Smargo & other Usb card readers chipset ftdi:"), self.ftdi_sio)
		self.list.append(res)
		res = getConfigListEntry(_("Other Usb card readers chipset pl2303:"), self.pl2303)
		self.list.append(res)
		res = getConfigListEntry(_("Tun module needed for Openvpn:"), self.tun)
		self.list.append(res)
		res = getConfigListEntry(_("Exportfs module needed for Nfs-Server:"), self.exportfs)
		self.list.append(res)
		res = getConfigListEntry(_("Nfsd module needed for Nfs-Server:"), self.nfsd)
		self.list.append(res)
		
		
		
		self["config"].list = self.list
		self["config"].l.setList(self.list)
		
		
	def saveMyconf(self):
		l1 = ""; l2 = ""; l3 = ""; l4 = ""; l5 = ""; l6 = "";
		if self.ntfs.value == True:
			l1 = "modprobe ntfs"
			system(l1)
		else:
			system("rmmod ntfs")
			
		if self.ftdi_sio.value == True:
			l2 = "modprobe ftdi_sio"
			system(l2)
		else:
			system("rmmod ftdi_sio")
		
		if self.pl2303.value == True:
			l3 = "modprobe pl2303"
			system(l3)
		else:
			system("rmmod pl2303")
			
		if self.tun.value == True:
			l4 = "modprobe tun"
			system(l4)
		else:
			system("rmmod tun")
		
		if self.exportfs.value == True:
			l5 = "modprobe exportfs"
			system(l5)
		else:
			system("rmmod exportfs")
			
		if self.nfsd.value == True:
			l6 = "modprobe nfsd"
			system(l6)
		else:
			system("rmmod nfsd")
			system("rmmod exportfs")
		
		
		out = open("/usr/bin/bhextramod",'w')
		out.write("#!/bin/sh" + "\n")
		if l1 != "":
			out.write(l1 + "\n")
		if l2 != "":
			out.write(l2 + "\n")
		if l3 != "":
			out.write(l3 + "\n")
		if l4 != "":
			out.write(l4 + "\n")
		if l5 != "":
			out.write(l5 + "\n")
		if l6 != "":
			out.write(l6 + "\n")
		
		out.close()
		system("chmod 0755 /usr/bin/bhextramod")
		
		self.close()

class DeliteKernelModShow(Screen):
	skin = """
	<screen position="339,160" size="602,410" title="Active Kernel Modules">
		<widget source="list" render="Listbox" position="10,10" size="580,320" zPosition="1" scrollbarMode="showOnDemand" transparent="1">
			<convert type="TemplatedMultiContent">
				{"template": [
				MultiContentEntryText(pos = (10, 2), size = (570, 30), flags = RT_HALIGN_LEFT|RT_VALIGN_CENTER, text = 0),
				],
				"fonts": [gFont("Regular", 24)],
				"itemHeight": 30
				}
			</convert>
		</widget>
		<widget name="statuslab" position="10,340" size="580,70" font="Regular;20" valign="center" backgroundColor="#333f3f3f" foregroundColor="#FFC000" shadowOffset="-3,-3" shadowColor="black"/>
	</screen>"""
	
	def __init__(self, session):
		Screen.__init__(self, session)

		self.list = []
		self["list"] = List(self.list)
		self["list"].onSelectionChanged.append(self.schanged)
		self["statuslab"] = Label("")
		self.updateList()
		self["actions"] = ActionMap(["WizardActions"],
		{
			"ok": self.close,
			"back": self.close,

		})		
		
		self.onLayoutFinish.append(self.refr_sel)
		
	def refr_sel(self):
		self["list"].index = 1
		self["list"].index = 0
			

	def updateList(self):
		
		rc = system("lsmod > /tmp/ninfo.tmp")
		strview = ""
		if fileExists("/tmp/ninfo.tmp"):
			f = open("/tmp/ninfo.tmp",'r')
 			for line in f.readlines():
				parts = line.strip().split()
				if parts[0] == "Module":
					continue
				res = (parts[0], line)
				self.list.append(res)
 			f.close()
			os_remove("/tmp/ninfo.tmp")
			self["list"].list = self.list
			
		
	def schanged(self):
		mysel = self["list"].getCurrent()
		if mysel:
			mytext = mysel[1]
			parts = mytext.split()
			size = parts[1]
			pos = len(parts[0]) + len(parts[1])
			used = mytext[pos:]
		
			mytext = "Module size: " + size + " bytes\n" + "Module used by: " + used
			self["statuslab"].setText(mytext)
			
class DeliteDtt(Screen):
	skin = """
	<screen position="center,center" size="710,340" title="Black Hole External Usb DVB Tuner Panel">
		<widget name="lab1" position="10,10" size="690,180" font="Regular;24" valign="center" transparent="1"/>
		<widget name="lab2" position="20,210" size="300,32" font="Regular;24" valign="center" transparent="1"/>
		<widget name="labstop" position="330,210" size="140,32" font="Regular;24" valign="center"  halign="center" backgroundColor="red"/>
		<widget name="labrun" position="330,210" size="140,32" zPosition="1" font="Regular;24" valign="center"  halign="center" backgroundColor="green"/>
		<ePixmap position="73,280" size="250,40" pixmap="skin_default/buttons/red.png" alphatest="on" zPosition="1" />
		<ePixmap position="285,280" size="250,40" pixmap="skin_default/buttons/green.png" alphatest="on" zPosition="1" />
		<ePixmap position="497,280" size="250,40" pixmap="skin_default/buttons/yellow.png" alphatest="on" zPosition="1" />
		<widget name="key_red" position="73,281" zPosition="2" size="140,40" font="Regular;20" halign="center" valign="center" backgroundColor="red" transparent="1" />
		<widget name="key_green" position="285,281" zPosition="2" size="140,40" font="Regular;20" halign="center" valign="center" backgroundColor="green" transparent="1" />
		<widget name="key_yellow" position="497,281" zPosition="2" size="140,40" font="Regular;20" halign="center" valign="center" backgroundColor="#a08500" transparent="1"/>
	</screen>"""
	
	def __init__(self, session):
		Screen.__init__(self, session)
		
		self.mess = "Usb Tuner Drivers not installed"
		self["lab1"] = Label(self.mess)
		self["lab2"] = Label(_("Current Status:"))
		self["labstop"] = Label("Disabled")
		self["labrun"] = Label("Working")
		self["key_red"] = Label("Select driver")
		self["key_green"] = Label("Enable")
		self["key_yellow"] = Label("Disable")
		self.my_dtt_active = False
				
		self["actions"] = ActionMap(["WizardActions", "ColorActions"],
		{
			"ok": self.close,
			"back": self.close,
			"red": self.MeInstall,
			"green": self.MeStart,
			"yellow": self.MeStop
		})
		
		self.onLayoutFinish.append(self.updateMe)
		
	def MeInstall(self):
		self.session.openWithCallback(self.updateMe, DeliteDttMainConf)
		
	
	def updateMe(self):
		self.mess = "Usb Tuner Drivers not installed"
		if fileExists("/usr/bin/bhusbdvb.sh"):
			f = open("/usr/bin/bhusbdvb.sh",'r')
			for line in f.readlines():
				if line.find("#description:") != -1:
					parts = line.strip().split(':')
					self.mess = "Drivers: " + parts[1]
					break
			f.close()
		if fileExists("/etc/bh_usb_dvb.cfg"):
			f = open("/etc/bh_usb_dvb.cfg",'r')
			line = f.read()
			self.mess = "Current Cfg: " + line + "\n" + self.mess
			f.close()
		
		self["lab1"].setText(self.mess)
		
		self["labrun"].hide()
		self["labstop"].hide()
		self.my_dtt_active = False
		rc = system("ps > /tmp/nvpn.tmp")
		f = open("/tmp/nvpn.tmp",'r')
		for line in f.readlines():
			if line.find('usbtuner') != -1:
				self.my_dtt_active = True		
		f.close()
			
		if self.my_dtt_active == True:
			self["labstop"].hide()
			self["labrun"].show()
		else:
			self["labstop"].show()
			self["labrun"].hide()
	
	def MeStart(self):
		if self.mess == "Usb Tuner Drivers not installed":
			nobox = self.session.open(MessageBox, "You have to select a driver before to activate", MessageBox.TYPE_INFO)
			nobox.setTitle("Info")
		else:
			if self.my_dtt_active == False:
				m = "echo -e '\n\nProbing Usb Tuner.........\n\nPlease wait.........\n'"
				m1 = "/usr/bin/bhusbdvb.sh"
				m2 = "sleep 2"
				self.session.open(Console, title="Dtt", cmdlist=[m,m1,m2], finishedCallback = self.MeStart2)
			
	
	
	def MeStart2(self):
		check = False
		rc = system("ps > /tmp/nvpn.tmp")
		f = open("/tmp/nvpn.tmp",'r')
		for line in f.readlines():
			if line.find('usbtuner') != -1:
				check = True		
		f.close()
		if check == True:
			out = open("/usr/bin/enigma2sh.tmp", "w")
			f = open("/usr/bin/enigma2.sh",'r')
			for line in f.readlines():
				if line.find("bhusbdvb.sh") != -1:
					continue
				if line.find("-d /home/root") != -1:
					out.write("/usr/bin/bhusbdvb.sh\n")
				out.write(line)
			f.close()
			out.close()
			os_rename("/usr/bin/enigma2sh.tmp", "/usr/bin/enigma2.sh")
			system("chmod 0755 /usr/bin/enigma2.sh")
			message = "Tuner activation need gui restart to take effects.\nRestart Gui now?"
			ybox = self.session.openWithCallback(self.restEn, MessageBox, message, MessageBox.TYPE_YESNO)
			ybox.setTitle("Gui Restart.")
		else:
			mybox = self.session.open(MessageBox, "Sorry, No supported device found.", MessageBox.TYPE_INFO)
			mybox.setTitle("Info")
			self.close()
	
	def MeStop(self):
		if self.my_dtt_active == True:
			out = open("/usr/bin/enigma2sh.tmp", "w")
			f = open("/usr/bin/enigma2.sh",'r')
			for line in f.readlines():
				if line.find("bhusbdvb.sh") != -1:
					continue
				out.write(line)
			f.close()
			out.close()
			os_rename("/usr/bin/enigma2sh.tmp", "/usr/bin/enigma2.sh")
			system("chmod 0755 /usr/bin/enigma2.sh")
			message = "Tuner deactivation need a reboot to take effects.\nReboot your box now?"
			ybox = self.session.openWithCallback(self.restBo, MessageBox, message, MessageBox.TYPE_YESNO)
			ybox.setTitle("Reboot.")
	
	def restEn(self, answer):
		if answer is True:
			self.session.open(TryQuitMainloop, 3)
		else:
			self.close()
			
	def restBo(self, answer):
		if answer is True:
			self.session.open(TryQuitMainloop, 2)
		else:
			self.close()
	
class DeliteDttMainConf(Screen):
	skin = """
	<screen position="center,center" size="800,520" title="Black Hole Usb Tuners Config">
           <widget source="list" render="Listbox" position="20,20" size="760,510" scrollbarMode="showOnDemand" >
            	<convert type="TemplatedMultiContent">
                    {"template": [
                       MultiContentEntryText(pos = (90, 25), size = (690, 80), font=0, text = 0),
                        MultiContentEntryPixmapAlphaTest(pos = (0, 3), size = (80, 80), png = 1),
                    ],
                    "fonts": [gFont("Regular", 24),gFont("Regular", 24)],
                    "itemHeight": 86
                    }
                    </convert>
           </widget>
         	<ePixmap position="100,460" size="250,40" pixmap="skin_default/buttons/red25.png" alphatest="on" zPosition="1" />
        	<ePixmap position="450,460" size="250,40" pixmap="skin_default/buttons/yellow25.png" alphatest="on" zPosition="1" />
		<widget name="key_red" position="100,468" zPosition="2" size="250,40" font="Regular;24" halign="center" valign="center" backgroundColor="transpBlack" transparent="1" />
		<widget name="key_yellow" position="450,468" zPosition="2" size="250,40" font="Regular;24" halign="center" valign="center" backgroundColor="transpBlack" transparent="1" />
    	</screen>"""
	
	def __init__(self, session):
		Screen.__init__(self, session)
		
		self["key_red"] = Label(_("Continue"))
		self["key_yellow"] = Label(_("Cancel"))
		
		self.list = []
		self["list"] = List(self.list)
		
		self["actions"] = ActionMap(["WizardActions", "ColorActions"],
		{
			"back": self.close,
			"ok": self.KeyOk,
			"red": self.KeyOk,
			"yellow": self.close
		})
		
		self.updateList()
		
	def updateList(self):	
		self.list = [ ]
		mypath = DeliteGetSkinPath()
		
		mypixmap = mypath + "icons/usbtuner_one_mono.png"
		png = LoadPixmap(mypixmap)
		name = "One Usb stick mono-tuner"
		idx = 0
		res = (name, png, idx)
		self.list.append(res)
		
		mypixmap = mypath + "icons/usbtuner_one_dual.png"
		png = LoadPixmap(mypixmap)
		name = "One Usb stick dual-tuner"
		idx = 1
		res = (name, png, idx)
		self.list.append(res)
		
		mypixmap = mypath + "icons/usbtuner_dual_same.png"
		png = LoadPixmap(mypixmap)
		name = "Two Usb sticks same model"
		idx = 2
		res = (name, png, idx)
		self.list.append(res)
		
		mypixmap = mypath + "icons/usbtuner_dual_different.png"
		png = LoadPixmap(mypixmap)
		name = "Two Usb sticks different models"
		idx = 3
		res = (name, png, idx)
		self.list.append(res)
		self["list"].list = self.list

	def KeyOk(self):
		self.sel = self["list"].getCurrent()
		if self.sel:
			self.sel = self.sel[2]
			self.session.open(DeliteDttDriversList, self.sel)
			
		self.close()

	
class DeliteDttDriversList(Screen):
	skin = """
	<screen position="center,center" size="860,540" title="Usb Tuner Available Drivers">
		<widget source="list" render="Listbox" position="10,10" size="840,500" scrollbarMode="showOnDemand" >
			<convert type="StringList" />
		</widget>
		<widget name="Linconn" position="10,500" size="840,30" font="Regular;20" halign="center" valign="center" backgroundColor="#9f1313" />
	</screen>"""
	
	def __init__(self, session, device):
		Screen.__init__(self, session)

		self.list = []
		self["list"] = List(self.list)
		self["Linconn"] = Label("Wait please, connection to server in progress ....")
		self["actions"] = ActionMap(["WizardActions"],
		{
			"ok": self.myinstall,
			"back": self.close,

		})
		self.activityTimer = eTimer()
		self.activityTimer.timeout.get().append(self.Listconn)
		self.activityTimer.start(1, False)
		self.onClose.append(self.delTimer)
		
		self.progress = 0
		self.device = device
		self.mainconf = "One Usb stick mono-tuner"
		if self.device == 1:
			self.mainconf = "One Usb stick dual-tuner"
		elif self.device == 2:
			self.mainconf = "Two Usb sticks same model"
		elif self.device == 3:
			self.mainconf = "Two Usb sticks different models"
			
	
	def delTimer(self):
		del self.activityTimer
		
	def DeliteDtt_geturl(self):
		machine = nab_Detect_Machine()
		ver = BhU_get_Version()
		path = "http://www.vuplus-community.net/driversusb/"
#		good = ["bm750", "vusolo"]
#		if machine in good:
#			path = "http://www.vuplus-community.net/driversusb/"
		
		if machine == "bm750":
			machine = "vuduo"
		path += ver + "/" + machine
		return path
	
	def Listconn(self):
		self.activityTimer.stop()
		url = self.DeliteDtt_geturl()
		url += "/driverslist.cfg"
		cmd = "wget -O /tmp/drvlist.tmp " + url
		rc = system(cmd)
		strview = ""
		if fileExists("/tmp/drvlist.tmp"):
			f = open("/tmp/drvlist.tmp",'r')
 			for line in f.readlines():
				if line.find(';') != -1:
					parts = line.strip().split(';')
					text = parts[0].strip() + "   by: " + parts[1].strip()
					file = parts[2].strip()
					res = (text, file)
					self.list.append(res)
 			f.close()
			os_remove("/tmp/drvlist.tmp")
			self["list"].list = self.list
			
		else:
			mybox = self.session.open(MessageBox, "Sorry. Connection to BH Server refused.\nCheck that your internet connection is up and running", MessageBox.TYPE_INFO)
			mybox.setTitle("Info")

		self["Linconn"].hide()
	
	def myinstall(self):
		self.sel = self["list"].getCurrent()
		if self.sel:
			message = "Do you want to install the Driver:\n " + self.sel[0] + " ?"
			ybox = self.session.openWithCallback(self.installadd2, MessageBox, message, MessageBox.TYPE_YESNO)
			ybox.setTitle("Installation Confirm")
			
	def installadd2(self, answer):
		if answer is True:
			if self.device == 0:
				self.compose_mono("1")
			elif self.device == 1:
				self.compose_mono("2")
			elif self.device == 2:
				self.compose_mono("2")
			elif self.device == 3:
				if self.progress == 0:
					self.progress = 1
					self.compose_mono("3")
				else:
					self.compose_dual()
				
			#self.session.open(MessageBox, self.device, MessageBox.TYPE_INFO)
			
	def write_cfg(self):
		out = open("/etc/bh_usb_dvb.cfg", "w")
		out.write(self.mainconf)
		out.close()
		
	def compose_mono(self, answer):
		system("rm -f /lib/modules/dvbt/*")
		system("rm -f /usr/bin/bhusbdvb.sh")
		system("killall -9 usbtuner")
		url = self.DeliteDtt_geturl()
		file = self.sel[1]
		file = file.strip()
		url = url + "/" + file
		cmd = "wget -O /tmp/" + file + " " + url
		rc = system(cmd)
		dest = "/tmp/" + file
		mydir = getcwd()
		chdir("/")
		cmd = "tar -xzf " + dest
		rc = system(cmd)
		chdir(mydir)
		cmd = "rm -f " + dest
		rc = system(cmd)
		system("chmod 0755 /usr/bin/bhusbdvb.sh")
		if answer == "3":
			os_rename("/usr/bin/bhusbdvb.sh", "/usr/bin/bhusbdvb.tmp2")
			mybox = self.session.open(MessageBox, "First tuner drivers installed.\n You can now select drivers for second tuner", MessageBox.TYPE_INFO)
			mybox.setTitle("Info")
		else:
			self.write_cfg()
			mybox = self.session.open(MessageBox, "Driver Successfully Installed.\n You can now Enable your Usb tuner", MessageBox.TYPE_INFO)
			mybox.setTitle("Info")
			self.close()
	
	def compose_dual(self):
		newdrivers = ""
		description = ""
		system("killall -9 usbtuner")
		url = self.DeliteDtt_geturl()
		file = self.sel[1]
		file = file.strip()
		url = url + "/" + file
		cmd = "wget -O /tmp/" + file + " " + url
		rc = system(cmd)
		dest = "/tmp/" + file
		mydir = getcwd()
		chdir("/")
		cmd = "tar -xzf " + dest
		rc = system(cmd)
		chdir(mydir)
		cmd = "rm -f " + dest
		rc = system(cmd)
		
		f = open("/usr/bin/bhusbdvb.sh",'r')
		check = 0
		for line in f.readlines():
			if line.find('#description:') != -1:
				description = line[13:]
			if line.find('# fine drivers') != -1:
				break
			if check == 1:
				newdrivers = newdrivers + line
			if line.find('# inizio drivers') != -1:
				check = 1
		f.close()
		
		out = open("/usr/bin/bhusbdvb.sh", "w")
		f = open("/usr/bin/bhusbdvb.tmp2",'r')
		for line in f.readlines():
			if line.find('#description:') != -1:
				line = line.strip() + " -" + description + "\n"
			if line.find("# fine drivers") != -1:
				out.write(newdrivers)
			out.write(line)
		f.close()
		out.close()
		system("chmod 0755 /usr/bin/bhusbdvb.sh")
		system("rm -f /usr/bin/bhusbdvb.tmp2")
		self.write_cfg()
		mybox = self.session.open(MessageBox, "Drivers for tuner1 and tuner2 successfully installed.\n You can now Enable your tuners", MessageBox.TYPE_INFO)
		mybox.setTitle("Info")
		self.close()
	
class BhHdmiCecConf(Screen, ConfigListScreen):
	skin = """
	<screen position="center,center" size="900,500" title="Black Hole Hdmi Cec Setup">
		<widget name="config" position="10,10" size="880,140" scrollbarMode="showOnDemand"/>
		<widget name="lab1" position="10,150" size="880,300" font="Regular;20" halign="center" valign="center" foregroundColor="green" />
		<ePixmap pixmap="skin_default/buttons/red.png" position="380,460" size="140,40" alphatest="on"/>
		<widget name="key_red" position="380,460" zPosition="1" size="140,40" font="Regular;20" halign="center" valign="center" backgroundColor="#9f1313" transparent="1"/>
	</screen>"""
	
	def __init__(self, session):
		Screen.__init__(self, session)
		
		self.list = []
		ConfigListScreen.__init__(self, self.list)
		
		labtxt = "Welcome in Black Hole Hdmi Cec.\nThe new Black Hole Hdmi Cec driver allows you to control both your Tv and your Vu+ box with the Tv remote control only. Not all Tv models compatible. Bh Hdmi-Cec works on ALL latest Samsung(Anynet+) and many other Tv models.\nInstructions to connect the box to your Hdmi-Cec compatible Tv:\n1) Enter in your Tv Menu Options and enable all the Hdmi-Cec options.\n2) Configure in this screen the right Hdmi connection port and enable Bh Hdmi-Cec.\n3) Click Save button and your box will try to connect with your Tv. All Done. If your Tv is compatible you can now control Tv and Box with Tv rc.\nWarning: You have to select the specific port option if your box is connected to an ampli.\nPlease report @vuplus-community.net your tests on your tv model."
		
		self["key_red"] = Label(_("Save"))
		self["lab1"] = Label(labtxt)
		
		self["actions"] = ActionMap(["WizardActions", "ColorActions"],
		{
			"red": self.saveMyosd,
			"back": self.close

		})
			
		self.updateList()
	
	
	def updateList(self):
		
		self.on = NoSave(ConfigYesNo(default="False"))
		self.tvstandby = NoSave(ConfigYesNo(default="False"))
		self.tvwakeup = NoSave(ConfigYesNo(default="False"))
		self.boxstandby = NoSave(ConfigYesNo(default="False"))
		self.port = NoSave(ConfigSelection(default = "1", choices = [
		("1", "Vu+ -> Tv Hdmi-1"), ("2", "Vu+ -> Tv Hdmi-2"), ("3", "Vu+ -> Tv Hdmi-3"), ("4", "Vu+ -> Tv Hdmi-4"),
		("5", "Vu+ -> Ampli Hdmi-1 -> Tv Hdmi-1"), ("6", "Vu+ -> Ampli Hdmi-1 -> Tv Hdmi-2"), ("7", "Vu+ -> Ampli Hdmi-1 -> Tv Hdmi-3"),
		("8", "Vu+ -> Ampli Hdmi-1 -> Tv Hdmi-4"), ("9", "Vu+ -> Ampli Hdmi-2 -> Tv Hdmi-2")]))
		
		self.tvstandby.value = config.hdmicec.tvstandby.value
		self.tvwakeup.value = config.hdmicec.tvwakeup.value
		self.boxstandby.value = config.hdmicec.boxstandby.value
		self.on.value = config.hdmicec.on.value
		self.port.value = config.hdmicec.port.value
		
		item = getConfigListEntry(_("Enable Black Hole Hdmi-Cec"), self.on)
		self.list.append(item)
		
		item = getConfigListEntry(_("Box connected to port:"), self.port)
		self.list.append(item)
		
		item = getConfigListEntry(_("1 Tv remote control standby \t->  standby Vu+ box"), self.tvstandby)
		self.list.append(item)
		
		item = getConfigListEntry(_("2 Tv remote control wakeup \t->  wakeup Vu+ box"), self.tvwakeup)
		self.list.append(item)
		
		item = getConfigListEntry(_("3 Vu+ remote control standby \t->  standby Tv"), self.boxstandby)
		self.list.append(item)
		
		
		self["config"].list = self.list
		self["config"].l.setList(self.list)
		
		
	def saveMyosd(self):
		
		config.hdmicec.tvstandby.value = self.tvstandby.value
		config.hdmicec.tvwakeup.value = self.tvwakeup.value
		config.hdmicec.boxstandby.value = self.boxstandby.value
		config.hdmicec.on.value = self.on.value
		config.hdmicec.port.value = self.port.value
		
		config.hdmicec.tvstandby.save()
		config.hdmicec.tvwakeup.save()
		config.hdmicec.boxstandby.save()
		config.hdmicec.on.save()
		config.hdmicec.port.save()		
		configfile.save()
				
		self.bhHdmiInit()
		
	def bhHdmiInit(self):
		from enigma import eHdmiCEC
		eHdmiCEC.getInstance().sendMessage(0x0F, 0x82)
		self.session.openWithCallback(self.bhClose, MessageBox, "Black Hole Hdmi-Cec inizialized.\nYou can now try to use your tv rc to control your Vu+ Box.", MessageBox.TYPE_INFO)

	
	def bhClose(self, answer):
		self.close()
