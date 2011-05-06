from Screens.Screen import Screen

from Screens.MessageBox import MessageBox
from Screens.VirtualKeyBoard import VirtualKeyBoard
from Components.ActionMap import ActionMap
from Components.Label import Label
from Components.Pixmap import Pixmap
from Components.Sources.List import List
from Components.ConfigList import ConfigListScreen
from Components.config import getConfigListEntry, config, ConfigYesNo, ConfigText, ConfigSelection, ConfigClock, NoSave, configfile
from Tools.Directories import fileExists
from os import system, remove as os_remove, rename as os_rename
from enigma import eEPGCache, eTimer, eServiceReference
from urllib2 import Request, urlopen, URLError, HTTPError
import time
import datetime


def nab_Get_EpgProvider(provider):
	f = open("/etc/Bhepgproviders.cfg",'r')
 	for line in f.readlines():
		parts = line.strip().split(",")
		if parts[0] == provider:
			break
	f.close()
	return parts

# available channel files (todo - update this list)
def nab_Get_Channelsfile(provider):
	myfile = None
	if provider == "Sky-Ita":
		myfile = "/usr/share/dict/channels.it"
	elif provider == "Sky-Uk":
		myfile = "/usr/share/dict/channels.uk"
	elif provider == "Sweden-tvsajten":
		myfile = "/usr/share/dict/channels.sw"
	elif provider == "Australia-Foxtel":
		myfile = "/usr/share/dict/channels.au"
	
	return myfile
		

class DeliteEpgPanel(Screen):
	skin = """
	<screen position="339,100" size="602,510" title="Black Hole E2 EPG Settings">
		<widget name="lsinactive" position="20,10" zPosition="1" pixmap="skin_default/icons/ninactive.png" size="32,32" alphatest="on"/>
		<widget name="lsactive" position="20,10" zPosition="2" pixmap="skin_default/icons/nactive.png" size="32,32" alphatest="on"/>
		<widget name="lab1" position="60,10" size="400,30" font="Regular;20" valign="center" transparent="1"/>
		<widget name="luinactive" position="20,50" zPosition="1" pixmap="skin_default/icons/ninactive.png" size="32,32" alphatest="on"/>
		<widget name="luactive" position="20,50" zPosition="2" pixmap="skin_default/icons/nactive.png" size="32,32" alphatest="on"/>
		<widget name="lab2" position="50,50" size="400,30" font="Regular;20" valign="center" transparent="1"/>
		<widget name="lpinactive" position="20,90" zPosition="1" pixmap="skin_default/icons/ninactive.png" size="32,32" alphatest="on"/>
		<widget name="lpactive" position="20,90" zPosition="2" pixmap="skin_default/icons/nactive.png" size="32,32" alphatest="on"/>
		<widget name="lab3" position="60,90" size="400,30" font="Regular;20" valign="center" transparent="1"/>    
		<widget name="lab4" position="20,130" size="260,30" font="Regular;20" valign="center" transparent="1"/>
		<widget name="labpath" position="290,130" size="190,30" font="Regular;20" valign="center" halign="center" backgroundColor="black"/>
		<widget name="lab5" position="20,170" size="260,30" font="Regular;20" valign="center" transparent="1"/>
		<widget source="list" render="Listbox" position="40,200" size="500,250" scrollbarMode="showOnDemand">
			<convert type="StringList"/>
		</widget>
		<ePixmap pixmap="skin_default/buttons/red.png" position="50,460" size="220,40" alphatest="on"/>
		<widget name="key_red" position="55,460" zPosition="1" size="220,40" font="Regular;20" halign="center" valign="center" backgroundColor="#9f1313" transparent="1"/>
		<ePixmap pixmap="skin_default/buttons/green.png" position="330,465" size="220,40" alphatest="on" />
		<widget name="key_green" position="330,460" zPosition="1" size="220,40" font="Regular;20" halign="center" valign="center" backgroundColor="#1f771f" transparent="1"/>
	</screen>"""
	
	def __init__(self, session):
		Screen.__init__(self, session)
		
		self["lsinactive"] = Pixmap()
		self["lsactive"] = Pixmap()
		self["lab1"] = Label(_("Enable OpenTv Epg Loader"))
		self["luinactive"] = Pixmap()
		self["luactive"] = Pixmap()
		self["lab2"] = Label(_("Enable Epg Popup Notifications"))
		self["lpinactive"] = Pixmap()
		self["lpactive"] = Pixmap()
		self["lab3"] = Label(_("Enable Epg Buttons in Channel list"))
		self["lab4"] = Label(_("Path to save Epg File:"))
		self["labpath"] = Label("")
		self["lab5"] = Label(_("Available Providers:"))
		self["key_red"] = Label(_("Global Settings"))
		self["key_green"] = Label(_("Provider Settings"))
		self["key_yellow"] = Label(_("Add"))
		self["key_blue"] = Label(_("Remove"))
		self.flist = []
		self["list"] = List(self.flist)
		
		self["actions"] = ActionMap(["WizardActions", "ColorActions"],
		{
			"back": self.close,
			"red": self.setupgen,
			"green": self.setupsingle,
			"yellow": self.addProvider,
			"blue": self.delProvider,
			"ok": self.setupsingle
		})

#opentv: Nome, tipo-epg, url, maxdays, lang
#xmltv:   Nome, tipo-epg, channel-name, channel-ref, 0

		if fileExists("/etc/Bhepgproviders.cfg") == False:
			out = open("/etc/Bhepgproviders.cfg", "w")
			out.write("Rytec_SKYIT,ext_dat,http://www.xmltvepg.be/italy/epg.dat.gz,7,none\n")
			out.write("Satmate_sky.IT,ext_dat,http://hqsatellite.com/satmate/skyit_epg.dat.gz,7,none\n")
			out.write("Rytec-SKYUK,ext_dat,http://www.xmltvepg.be/uk/epg.dat.gz,7,none\n")
			out.write("Rytec_SKYDE,ext_dat,http://www.xmltvepg.be/germany/epg.dat.gz,7,none\n")
			
			out.write("Sky-Ita,opentv,Marco Polo,1:0:1:E31:16A8:FBFF:820000:0:0:0:,0\n")
			out.write("Sky-Uk,opentv,Hip Hop,1:0:2:FD1:7D4:2:11A0000:0:0:0:,0\n")
			
			out.write("Rytec-BE-NL,ext_dat,http://www.xmltvepg.be/benl/epg.dat.gz,7,none\n")
			out.write("Rytec-BE-NL-SKYUK-Telesat,ext_dat,http://www.xmltvepg.be/benluk/epg.dat.gz,7,none\n")
			
			out.write("Rytec-CSAT,ext_dat,http://www.xmltvepg.be/csat/epg.dat.gz,7,none\n")
			out.write("Rytec-NORDIC,ext_dat,http://www.xmltvepg.be/nordic/epg.dat.gz,7,none\n")
			out.write("Rytec_Dplus,ext_dat,http://www.xmltvepg.be/dplus/epg.dat.gz,7,none\n")
			out.write("Rytec_NOVA,ext_dat,http://www.xmltvepg.be/nova/epg.dat.gz,7,none\n")
			out.write("Rytec_Poland,ext_dat,http://www.xmltvepg.be/poland/epg.dat.gz,7,none\n")
			
			
			out.write("Krkadoni-ExYu,ext_dat,http://krkadoni.com/ext.epg.dat.gz,7,none\n")
			out.write("Krkadoni-NL,ext_dat,http://krkadoni.com/nl.epg.dat.gz,7,none\n")
			out.write("Australia-Foxtel,opentv,Epg,1:0:1:4270:11:1000:6180000:0:0:0:,0\n")
#			out.write("Cyfra+,mhw,4Fun,1:0:1:1134:2af8:013e:820000:0:0:0:,0\n")
#			out.write("Csat,mhw,GuideTv,1:0:1:238d:44a:1:c00000:0:0:0:,0\n")
#			out.write("Canaldigitaal,mhw,Ned1,1:0:1:FAB:451:35:c00000:0:0:0:,0\n")
#			out.write("Digital+,mhw,Musica Digital,1:0:2:7594:422:1:C00000:0:0:0:,0\n")
#			out.write("Viasat,mhw,History,1:0:1:17A2:8:56:300000:0:0:0:,0\n")
#			out.write("Canal-Digital-Nordic,mhw,Discovery-Travel&Living,1:0:1:3F8:A:46:E080000:0:0:0:,0\n")
#			out.write("Sweden-tvsajten,xmltv,http://xmltv.tvsajten.com/xmltv/,3,sw\n")
#			out.write("Cro-private,ext_dat,http://www.krkadoni.com/ext.epg.dat.bz2,7,none\n")
#			out.write("Norway-mspc,xmltv,http://epg.mspc.no/xmltv/,3,no\n")
			out.close()
		self.onLayoutFinish.append(self.updatemyinfo)
		
	def updatemyinfo(self):
		self["lsinactive"].hide()
		self["lsactive"].hide()
		self["luinactive"].hide()
		self["luactive"].hide()
		self["lpinactive"].hide()
		self["lpactive"].hide()
		
		myepgpath = config.misc.epgcache_filename.value
		
		if fileExists("/etc/skyitepglock"):
			self["lsinactive"].show()
		else:
			self["lsactive"].show()
		
		if config.misc.deliteepgpop.value == True:
			self["luactive"].show()
		else:
			self["luinactive"].show()
		
		
		self["labpath"].setText(myepgpath)
		
		if config.misc.deliteepgbuttons.value == True:
			self["lpactive"].show()
		else:
			self["lpinactive"].show()
		
		self.flist = []	
		f = open("/etc/Bhepgproviders.cfg",'r')
 		for line in f.readlines():
			parts = line.strip().split(",")
			res = (parts[0], parts[1], parts[2], parts[3], parts[4])
			self.flist.append(res)
		f.close()
		
		self["list"].list = self.flist
		
	def setupgen(self):
		self.session.openWithCallback(self.updatemyinfo, DeliteEpgGlobalSetup)
		
	def addProvider(self):
		self.session.openWithCallback(self.updatemyinfo, DeliteEpgAddProvider)
		
	def delProvider(self):
		self.sel = self["list"].getCurrent()
		if self.sel:
			etype = self.sel[1]
			if etype != "ext_dat":
				self.session.open(MessageBox, "Sorry you are allowed to remove external epg.dat servers only.", MessageBox.TYPE_ERROR)
			else:
				message = "Are you sure you want to Remove Server:\n " + self.sel[0] + "?"
				ybox = self.session.openWithCallback(self.dodelProvider, MessageBox, message, MessageBox.TYPE_YESNO)
				ybox.setTitle("Remove Confirmation")	
		
	def dodelProvider(self, answer):
		if answer is True:
			self.sel = self["list"].getCurrent()
			if self.sel:
				out = open("/etc/Bhepgproviders.tmp", "w")
				f = open("/etc/Bhepgproviders.cfg",'r')
				for line in f.readlines():
					parts = line.strip().split(",")
					if parts[0] != self.sel[0]:
						out.write(line)
				f.close()
				out.close()
				rc = system("mv -f  /etc/Bhepgproviders.tmp /etc/Bhepgproviders.cfg")
				
				out = open("/etc/bhcron/bh.cron", "w")
				if fileExists("/etc/bhcron/root"):
					f = open("/etc/bhcron/root",'r')
					for line in f.readlines():
						if line.find(self.sel[0]) != -1:
							continue	
						out.write(line)	
					f.close()
				out.close()
				rc = system("crontab /etc/bhcron/bh.cron -c /etc/bhcron/")
				
				self.flist = []	
				f = open("/etc/Bhepgproviders.cfg",'r')
 				for line in f.readlines():
					parts = line.strip().split(",")
					res = (parts[0], parts[1], parts[2], parts[3], parts[4])
					self.flist.append(res)
				f.close()
		
				self["list"].list = self.flist
		
	def setupsingle(self):
		self.sel = self["list"].getCurrent()
		if self.sel:
			etype = self.sel[1]
			if etype == "ext_dat":
				self.session.open(DeliteExtdatProv, self.sel[0])
			elif etype == "xmltv":
				self.session.open(DeliteXmltepgProv, self.sel[0])
			else:
				self.session.open(DeliteOpenepgProv, self.sel[0])


class DeliteEpgAddProvider(Screen, ConfigListScreen):
	skin = """
	<screen position="center,center" size="800,340" title="Black Hole EpgPanel: Add External epg Server">
		<widget name="lab1" position="10,20" size="780,100" font="Regular;20" halign="center" transparent="1"/>
		<widget name="config" position="10,130" size="780,120" scrollbarMode="showOnDemand" />
		<ePixmap pixmap="skin_default/buttons/red.png" position="100,270" size="140,40" alphatest="on" />
		<widget name="key_red" position="100,270" zPosition="1" size="140,40" font="Regular;20" halign="center" valign="center" backgroundColor="#9f1313" transparent="1" />
		<ePixmap pixmap="skin_default/buttons/green.png" position="560,270" size="140,40" alphatest="on" />
		<widget name="key_green" position="560,270" zPosition="1" size="140,40" font="Regular;20" halign="center" valign="center" backgroundColor="#1f771f" transparent="1"/>
	</screen>"""
	
	def __init__(self, session):
		Screen.__init__(self, session)
		
		self.list = []
		ConfigListScreen.__init__(self, self.list)
		self["lab1"] = Label("You can add here servers to download external epg.dat files.\nWarning: file format allowed are gzip and bzip2 epg.dat (.dat.gz .dat.bz2).\nExample: http://example.com/uk_epg.dat.gz")
		self["key_red"] = Label(_("Virtual Keyb."))
		self["key_green"] = Label(_("Save"))
		
		self["actions"] = ActionMap(["WizardActions", "ColorActions"],
		{
			"red": self.vkeyb,
			"back": self.close,
			"green": self.checkentry

		})
		self.updateList()


	def updateList(self):
		self.provider = NoSave(ConfigText(fixed_size = False))
		self.url = NoSave(ConfigText(fixed_size = False))
		self.provider.value = "None"
		self.url.value = "http://"
		
		res = getConfigListEntry("Server Name", self.provider)
		self.list.append(res)
		res = getConfigListEntry("Epg.dat Url", self.url)
		self.list.append(res)
		
		self["config"].list = self.list
		self["config"].l.setList(self.list)


	def vkeyb(self):
		sel = self["config"].getCurrent()
		if sel:
			self.vkvar = sel[0]
			value = "xmeo"
			if self.vkvar == "Server Name":
				value = self.provider.value
			elif self.vkvar == "Epg.dat Url":
				value = self.url.value
			
			if value == "None":
					value = ""
			
			if value != "xmeo":
				self.session.openWithCallback(self.UpdateAgain, VirtualKeyBoard, title=self.vkvar, text=value)

	def UpdateAgain(self, newt):
		self.list = [ ]
		if newt is None:
			newt = ""
		if newt.strip() != "":
			if self.vkvar == "Server Name":
				self.provider.value = newt
			elif self.vkvar == "Epg.dat Url":
				self.url.value = newt
			
			res = getConfigListEntry("Server Name", self.provider)
			self.list.append(res)
			res = getConfigListEntry("Epg.dat Url", self.url)
			self.list.append(res)
		
			self["config"].list = self.list
			self["config"].l.setList(self.list)
	
	def checkentry(self):
		msg = ""
		if self.provider.value.strip() == "None":
			self.provider.value = ""
		if self.url.value.strip() == "http://":
			self.url.value = ""
		if self.provider.value.strip() == "" or self.url.value.strip() == "":
			msg = "You have to provide both Server Name and Epg.dat Url"

		if self.url.value.find('.dat.gz') == -1 and self.url.value.find('.dat.bz2') == -1:
			msg = "Wrong file format.\n  Only epg.dat gzip and bzip2 files are allowed (.dat.gz .dat.bz2)."

		f = open("/etc/Bhepgproviders.cfg",'r')
 		for line in f.readlines():
			parts = line.strip().split(",")
			if parts[0] == self.provider.value:
				msg = "Error. This Provider name already exists in the list."
		f.close()


		if msg:
			self.session.open(MessageBox, msg, MessageBox.TYPE_ERROR)
		else:
			self.saveMyprov()
			
	def saveMyprov(self):
		line = self.provider.value + ",ext_dat," + self.url.value + ",7,none\n"
		out = open("/etc/Bhepgproviders.cfg", "a")
		out.write(line)
		out.close()
		self.close()


class DeliteEpgGlobalSetup(Screen, ConfigListScreen):
	skin = """
	<screen position="339,190" size="602,340" title="Black Hole E2 EPG Setup">
		<widget name="config" position="10,20" size="580,280" scrollbarMode="showOnDemand" />
		<ePixmap pixmap="skin_default/buttons/red.png" position="235,290" size="150,40" alphatest="on" />
		<widget name="key_red" position="235,290" zPosition="1" size="150,40" font="Regular;20" halign="center" valign="center" backgroundColor="#9f1313" transparent="1" />
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
		self.deliteepgdisabled = NoSave(ConfigYesNo(default=True))
		self.delitepopdisabled = NoSave(ConfigYesNo(default=True))
		self.deliteepgbuttons = NoSave(ConfigYesNo(default=True))
		
		my_tmp_path = config.misc.epgcache_filename.value
		
		self.myepg_path = NoSave(ConfigSelection(default = "/hdd/epg.dat", choices = [
		(my_tmp_path, my_tmp_path), ("/hdd/epg.dat", "/hdd/epg.dat"), ("/media/cf/epg.dat", "/media/cf/epg.dat"), ("/media/usb/epg.dat", "/media/usb/epg.dat"), ("/media/card/epg.dat", "/media/card/epg.dat"), ("/media/net/epg.dat", "/media/net/epg.dat")]))
		
		if fileExists("/etc/skyitepglock"):
			self.deliteepgdisabled.value = False
		else:
			self.deliteepgdisabled.value = True
		
		self.delitepopdisabled.value = config.misc.deliteepgpop.value
		self.deliteepgbuttons.value = config.misc.deliteepgbuttons.value
		
		self.myepg_path.value = my_tmp_path
		
		epg_disabled = getConfigListEntry(_("Enable OpenTv Epg Loader"), self.deliteepgdisabled)
		self.list.append(epg_disabled)
		
		pop_disabled = getConfigListEntry(_("Enable Epg Popup Notifications"), self.delitepopdisabled)
		self.list.append(pop_disabled)
		
		epg_buttons = getConfigListEntry(_("Enable Epg Buttons in Channel list"), self.deliteepgbuttons)
		self.list.append(epg_buttons)
		
		epg_path = getConfigListEntry(_("Path to save Epg File"), self.myepg_path)
		self.list.append(epg_path)
		
		self["config"].list = self.list
		self["config"].l.setList(self.list)
	
	
	def saveMyosd(self):
		config.misc.deliteepgpop.value = self.delitepopdisabled.value
		config.misc.deliteepgpop.save()
		config.misc.deliteepgbuttons.value = self.deliteepgbuttons.value
		config.misc.deliteepgbuttons.save()
		config.misc.epgcache_filename.value = self.myepg_path.value
		config.misc.epgcache_filename.save()
		configfile.save()
		
		if fileExists("/etc/skyitepglock"):
			if self.deliteepgdisabled.value == True:
				os_remove("/etc/skyitepglock")
		else:
			if self.deliteepgdisabled.value == False:
				out = open("/etc/skyitepglock", "w")
				out.write("Black Hole is the Best")
				out.close()
		
		self.close()
			
			
#------------------------------------- OPEN-TV EPG----------------------------------------------

class DeliteOpenepgProv(Screen):
	skin = """
	<screen position="339,150" size="602,400" title="Black Hole E2 EPG Settings">
		<widget name="lab1" position="20,10" size="240,30" font="Regular;20" transparent="1"/>
		<widget name="labprov" position="260,10" size="340,30" font="Regular;20"/>
		<widget name="lab1a" position="20,50" size="240,30" font="Regular;20" transparent="1"/>
		<widget name="labtype" position="260,50" size="340,30" font="Regular;20"/>
		<widget name="lab2" position="20,90" size="240,30" font="Regular;20" valign="center" transparent="1"/>
		<widget name="labchan" position="260,90" size="340,30" font="Regular;20" valign="center"/>
		<widget name="lsinactive" position="10,130" zPosition="1" pixmap="skin_default/icons/ninactive.png" size="32,32" alphatest="on"/>
		<widget name="lsactive" position="10,130" zPosition="2" pixmap="skin_default/icons/nactive.png" size="32,32" alphatest="on"/>
		<widget name="lab3" position="50,130" size="400,30" font="Regular;20" valign="center" transparent="1"/>
		<widget name="lab4" position="20,170" size="380,30" font="Regular;20" valign="center" transparent="1"/>
		<widget name="labtimes" position="430,170" size="60,30" font="Regular;20" valign="center" backgroundColor="black"/>
		<widget name="lab5" position="20,210" size="420,30" font="Regular;20" valign="center" transparent="1"/>
		<widget name="labaction" position="430,210" size="170,30" valign="center" font="Regular;20"/>
		<ePixmap pixmap="skin_default/buttons/red.png" position="40,350" size="140,40" alphatest="on"/>
		<widget name="key_red" position="45,350" zPosition="1" size="140,40" font="Regular;20" halign="center" valign="center" backgroundColor="#9f1313" transparent="1"/>
		<ePixmap pixmap="skin_default/buttons/green.png" position="220,350" size="140,40" alphatest="on" />
		<widget name="key_green" position="225,350" zPosition="1" size="140,40" font="Regular;20" halign="center" valign="center" backgroundColor="#1f771f" transparent="1"/>
		<ePixmap pixmap="skin_default/buttons/yellow.png" position="380,350" size="200,40" alphatest="on"/>
		<widget name="key_yellow" position="385,350" zPosition="1" size="200,40" font="Regular;20" halign="center" valign="center" backgroundColor="#a08500" transparent="1"/>
	</screen>"""
	
	def __init__(self, session, provider):
		Screen.__init__(self, session)
		
		self.provider = provider
		self["lab1"] = Label(_("Provider Name:"))
		self["labprov"] = Label("")
		self["lab1a"] = Label(_("Epg Type:"))
		self["labtype"] = Label("")
		self["lab2"] = Label(_("Epg stream channel:"))
		self["labchan"] = Label("")
		self["lsinactive"] = Pixmap()
		self["lsactive"] = Pixmap()
		self["lab3"] = Label(_("Enable Automatic EPG Refresh"))
		self["lab4"] = Label(_("Refresh EPG every day at time:"))
		self["labtimes"] = Label("")
		self["lab5"] = Label(_("Command to execute after EPG Refresh:"))
		self["labaction"] = Label("")
		self["key_red"] = Label(_("Settings"))
		self["key_green"] = Label(_("Channels"))
		self["key_yellow"] = Label(_("Download now"))
		
		self["actions"] = ActionMap(["WizardActions", "ColorActions"],
		{
			"back": self.close,
			"red": self.setupmyprov,
			"green": self.setchans,
			"yellow": self.downloadNow
		})

		self.onLayoutFinish.append(self.updatemyinfo)
		
	def updatemyinfo(self):
		self["lsinactive"].hide()
		self["lsactive"].hide()
		strview = ""
		mytmpt = "n/a"
		mypostcom = "n/a"
		self["labprov"].setText(self.provider)
		myline = "DeliteEpg-" + self.provider
		
		if fileExists("/etc/enigma2/timers.xml"):
			f = open("/etc/enigma2/timers.xml",'r')
 			for line in f.readlines():
				if line.find(myline) != -1:
					strview = line
					break
 			f.close()
		if strview:
			parts = strview.strip().split()
			mytmpt = parts[1].replace('"', '')
			mytmpti = int(mytmpt.replace('begin=', ''))	
			mytmpt = time.strftime("%H:%M %S", time.localtime(mytmpti))
			mytmpt = mytmpt[0:5]
			where = strview.find('afterevent=') + 12
			where2 = strview.find('"', where)
			mypostcom = strview[where:where2]
			self["lsactive"].show()
		else:
			self["lsinactive"].show()
		
		self["labtimes"].setText(mytmpt)
		self["labaction"].setText(mypostcom)
		
		parts = nab_Get_EpgProvider(self.provider)
		self["labtype"].setText(parts[1])
		self["labchan"].setText(parts[2])
		self.chanref = parts[3]
		
		
	def downloadNow(self):
		self.session.open(DeliteDownEpgNow, self.provider)
	
	def setupmyprov(self):
		self.session.openWithCallback(self.updatemyinfo, DeliteOepgSetup, self.provider, self.chanref)
		
		
	def setchans(self):
		myfile = nab_Get_Channelsfile(self.provider)
		if myfile:
			self.session.open(DeliteEpgChannels, self.provider)
		else:
			self.session.open(MessageBox, "Sorry, Channel List not available for this Provider.", MessageBox.TYPE_INFO)
		
class DeliteOepgSetup(Screen, ConfigListScreen):
	skin = """
	<screen position="339,190" size="602,340" title="Black Hole E2 EPG Setup">
		<widget name="lab1" position="10,10" size="240,30" font="Regular;20" transparent="1"/>
		<widget name="labprov" position="260,10" size="340,30" font="Regular;20"/>
		<widget name="config" position="10,40" size="580,250" scrollbarMode="showOnDemand" />
		<ePixmap pixmap="skin_default/buttons/red.png" position="235,290" size="150,40" alphatest="on" />
		<widget name="key_red" position="235,290" zPosition="1" size="150,40" font="Regular;20" halign="center" valign="center" backgroundColor="#9f1313" transparent="1" />
	</screen>"""
	
	def __init__(self, session, provider, chanref):
		Screen.__init__(self, session)
		
		self.provider = provider
		self.chanref = chanref
		self.list = []
		ConfigListScreen.__init__(self, self.list)
		self["key_red"] = Label(_("Save"))
		self["lab1"] = Label(_("Provider Name:"))
		self["labprov"] = Label(provider)
		self["actions"] = ActionMap(["WizardActions", "ColorActions"],
		{
			"red": self.saveMyprov,
			"back": self.close

		})
			
		self.updateList()
		

	def updateList(self):
	
		self.epgautodown = NoSave(ConfigYesNo(default=False))
		self.timerentry_starttime = NoSave(ConfigClock(default=0))
		self.delitepostcom = NoSave(ConfigSelection(default = "nothing", choices = [
		("nothing", "nothing"), ("standby", "standby"), ("deepstandby", "deepstandby")]))
		
		strview = ""
		mytmpt = [23,10]
		mypostcom = "n/a"
		autodown = False
		timername = "DeliteEpg-" + self.provider
		
		if fileExists("/etc/enigma2/timers.xml"):
			f = open("/etc/enigma2/timers.xml",'r')
 			for line in f.readlines():
				if line.find(timername) != -1:
					strview = line
					break
 			f.close()
		
		if strview:
			parts = strview.strip().split()
			mytmpt = parts[1].replace('"', '')
			mytmpti = int(mytmpt.replace('begin=', ''))	
			mytmpt = time.strftime("%H %M %S", time.localtime(mytmpti))
			mytmpt = mytmpt[0:5]
			parts2 = mytmpt.strip().split()
			mytmpt = [int(parts2[0]), int(parts2[1])]
			mypostcom = parts[7]
			where = strview.find('afterevent=') + 12
			where2 = strview.find('"', where)
			mypostcom = strview[where:where2]
			autodown = True
		
		self.epgautodown.value = autodown
		self.timerentry_starttime.value = mytmpt
		self.delitepostcom.value = mypostcom
		
		epg_autodown = getConfigListEntry(_("Enable Automatic EPG Refresh"), self.epgautodown)
		self.list.append(epg_autodown)
		starttime = getConfigListEntry(_("Refresh EPG every day at time"), self.timerentry_starttime)
		self.list.append(starttime)
		epg_postcom = getConfigListEntry(_("Command to execute after EPG Refresh"), self.delitepostcom)
		self.list.append(epg_postcom)
		
		self["config"].list = self.list
		self["config"].l.setList(self.list)
	
	
	def getTimestamp(self, date, mytime):
		d = time.localtime(date)
		dt = datetime.datetime(d.tm_year, d.tm_mon, d.tm_mday, mytime[0], mytime[1])
		return int(time.mktime(dt.timetuple()))	
	
	
	def saveMyprov(self):		
		timername = "DeliteEpg-" + self.provider
		starttime = self.timerentry_starttime.value
		begin = self.getTimestamp(time.time(), starttime)
		end = begin + 240
		postcom = self.delitepostcom.value
		
		if fileExists("/etc/enigma2/timers.xml") == False:
			out = open("/etc/enigma2/timers.xml",'w')
			out.write('<?xml version="1.0" ?>\n<timers>\n</timers>\n')
			out.close()		
		
		inme = open("/etc/enigma2/timers.xml",'r')
		out = open("/etc/enigma2/timers.tmp",'w')
		check = False
		for line in inme.readlines():
			if line.find(timername) != -1:
				check = True
				continue
			if check == True:
				check = False
				continue
			if line.find('</timers>') != -1:
				break
			out.write(line)
			
		if self.epgautodown.value == True:
			line = '<timer begin="' + str(begin) + '" end="' + str(end) + '" serviceref="' + self.chanref + '" repeated="127" name="' + timername + '" description="Dream Elite EPG SCHEDULER" afterevent="' + postcom + '" eit="720" location="/hdd/movie/" disabled="0" justplay="1">\n</timer>\n'
			out.write(line)
		out.write("</timers>\n")
		out.close()
		inme.close()
		os_rename("/etc/enigma2/timers.tmp", "/etc/enigma2/timers.xml")
		
		
		ybox = self.session.openWithCallback(self.restEn, MessageBox, "Click Ok to restart Enigma2 and activate changes.", MessageBox.TYPE_INFO)
		ybox.setTitle("Enigma2 Restart.")
					
	def restEn(self, answer):
#Warning E2 brutal kill is needed to make safe the new timers.xml file.
		system("killall -9 enigma2")
	
	
#--------------------------------------- EXTDAT EPG----------------------------------------------	

class DeliteExtdatProv(Screen):
	skin = """
	<screen position="center,center" size="800,400" title="Black Hole E2 EPG Settings">
		<widget name="lab1" position="20,10" size="240,30" font="Regular;20" transparent="1"/>
		<widget name="labprov" position="260,10" size="530,30" font="Regular;20"/>
		<widget name="lab1a" position="20,50" size="240,30" font="Regular;20" transparent="1"/>
		<widget name="labtype" position="260,50" size="340,30" font="Regular;20"/>
		<widget name="lab2" position="20,90" size="240,30" font="Regular;20" valign="center" transparent="1"/>
		<widget name="laburl" position="260,90" size="530,30" font="Regular;20" valign="center"/>	
		<widget name="lsinactive" position="10,210" zPosition="1" pixmap="skin_default/icons/ninactive.png" size="32,32" alphatest="on"/>
		<widget name="lsactive" position="10,210" zPosition="2" pixmap="skin_default/icons/nactive.png" size="32,32" alphatest="on"/>
		<widget name="lab5" position="50,210" size="400,30" font="Regular;20" valign="center" transparent="1"/>
		<widget name="lab6" position="20,250" size="380,30" font="Regular;20" valign="center" transparent="1"/>
		<widget name="labtimes" position="430,250" size="60,30" font="Regular;20" valign="center" backgroundColor="black"/>
		<ePixmap pixmap="skin_default/buttons/red.png" position="100,350" size="140,40" alphatest="on"/>
		<widget name="key_red" position="105,350" zPosition="1" size="140,40" font="Regular;20" halign="center" valign="center" backgroundColor="#9f1313" transparent="1"/>
		<ePixmap pixmap="skin_default/buttons/yellow.png" position="500,350" size="200,40" alphatest="on"/>
		<widget name="key_yellow" position="505,350" zPosition="1" size="200,40" font="Regular;20" halign="center" valign="center" backgroundColor="#a08500" transparent="1"/>
	</screen>"""

	def __init__(self, session, provider):
		Screen.__init__(self, session)
		
		self.provider = provider
		self["lab1"] = Label(_("Server Name:"))
		self["labprov"] = Label("")
		self["lab1a"] = Label(_("Epg Type:"))
		self["labtype"] = Label("")
		self["lab2"] = Label(_("Url:"))
		self["laburl"] = Label("")
		self["lsinactive"] = Pixmap()
		self["lsactive"] = Pixmap()
		self["lab5"] = Label(_("Enable Automatic EPG Refresh"))
		self["lab6"] = Label(_("Refresh EPG every day at time:"))
		self["labtimes"] = Label("")
		self["key_red"] = Label(_("Settings"))
		self["key_yellow"] = Label(_("Download now"))
		
		self["actions"] = ActionMap(["WizardActions", "ColorActions"],
		{
			"back": self.close,
			"red": self.setupmyprov,
			"yellow": self.downloadNow
		})

		self.onLayoutFinish.append(self.updatemyinfo)
		
	def updatemyinfo(self):
		self["lsinactive"].hide()
		self["lsactive"].hide()
		strview = ""
		mytmpt = "n/a"
		self["labprov"].setText(self.provider)
		
		parts = nab_Get_EpgProvider(self.provider)
		myurl = parts[2]
		self["labtype"].setText(parts[1])
		self["laburl"].setText(parts[2])
		
		if fileExists("/etc/bhcron/root"):
			f = open("/etc/bhcron/root",'r')
 			for line in f.readlines():
				if line.find(myurl) != -1:
					strview = line
					break
 			f.close()
		if strview:
			parts = strview.strip().split()
			mytmpt = parts[1] + ":" + parts[0]
			self["lsactive"].show()
		else:
			self["lsinactive"].show()
			
		self["labtimes"].setText(mytmpt)
		
	def downloadNow(self):
		self.session.open(DeliteDownEpgNow, self.provider)
		
		
	def setupmyprov(self):
		pass
		self.session.openWithCallback(self.updatemyinfo, DeliteExtdatSetup, self.provider)
		
class DeliteExtdatSetup(Screen, ConfigListScreen):
	skin = """
	<screen position="339,190" size="602,340" title="Black Hole E2 EPG Setup">
		<widget name="lab1" position="10,10" size="240,30" font="Regular;23" transparent="1"/>
		<widget name="labprov" position="260,10" size="340,30" font="Regular;20"/>
		<widget name="config" position="10,60" size="580,220" scrollbarMode="showOnDemand" />
		<ePixmap pixmap="skin_default/buttons/red.png" position="235,290" size="150,40" alphatest="on" />
		<widget name="key_red" position="235,290" zPosition="1" size="150,40" font="Regular;20" halign="center" valign="center" backgroundColor="#9f1313" transparent="1" />
	</screen>"""
	
	def __init__(self, session, provider):
		Screen.__init__(self, session)
		
		self.provider = provider
		self.list = []
		ConfigListScreen.__init__(self, self.list)
		self["key_red"] = Label(_("Save"))
		self["lab1"] = Label(_("Server Name:"))
		self["labprov"] = Label(provider)
		self["actions"] = ActionMap(["WizardActions", "ColorActions"],
		{
			"red": self.saveMyprov,
			"back": self.close
		})
			
		self.updateList()
	
	def updateList(self):
	
		self.epgautodown = NoSave(ConfigYesNo(default=False))
		self.timerentry_starttime = NoSave(ConfigClock(default=0))
		self.url = NoSave(ConfigText(fixed_size = False))
		
		strview = ""
		mytmpt = [23,20]
		autodown = False
		
		
		parts = nab_Get_EpgProvider(self.provider)
		myurl = parts[2]
		
		
		if fileExists("/etc/bhcron/root"):
			f = open("/etc/bhcron/root",'r')
 			for line in f.readlines():
				if line.find(self.provider) != -1:
					strview = line
					break
 			f.close()
		
		if strview:
			parts = strview.strip().split()
			mytmpt = [int(parts[1]), int(parts[0])]
			autodown = True
		
		self.epgautodown.value = autodown
		self.timerentry_starttime.value = mytmpt
		self.url.value = myurl
		
		
		epg_url = getConfigListEntry(_("Epg.dat Url"), self.url)
		self.list.append(epg_url)
		epg_autodown = getConfigListEntry(_("Enable Automatic EPG Refresh"), self.epgautodown)
		self.list.append(epg_autodown)
		starttime = getConfigListEntry(_("Refresh EPG every day at time"), self.timerentry_starttime)
		self.list.append(starttime)
		
		self["config"].list = self.list
		self["config"].l.setList(self.list)
		
	def saveMyprov(self):
		if self.url.value.find('.dat.gz') == -1 and self.url.value.find('.dat.bz2') == -1:
			msg = "Wrong file format.\n  Only epg.dat gzip and bzip2 files are allowed (.dat.gz .dat.bz2)."
			self.session.open(MessageBox, msg, MessageBox.TYPE_ERROR)
			return
		
		inme = open("/etc/Bhepgproviders.cfg",'r')
		out = open("/etc/Bhepgproviders.tmp",'w')
		for line in inme.readlines():
			parts = line.split(",")
			if parts[0] == self.provider:
				line = parts[0] + "," + parts[1] + "," + self.url.value + "," + parts[3] + "," + parts[4]
			out.write(line)
		out.close()
		inme.close()
		os_rename("/etc/Bhepgproviders.tmp", "/etc/Bhepgproviders.cfg")	
			
		parts = nab_Get_EpgProvider(self.provider)
		croncmd = "/usr/bin/Blackholecmd extepg," + parts[0] + "," + parts[2]
		hour = "%02d" % (self.timerentry_starttime.value[0])
		minutes =  "%02d" % (self.timerentry_starttime.value[1])
		newcron = minutes + " " + hour + " * * * " + croncmd + "\n"
		
		out = open("/etc/bhcron/bh.cron", "w")
		if fileExists("/etc/bhcron/root"):
			f = open("/etc/bhcron/root",'r')
			for line in f.readlines():
				if line.find(self.provider) != -1:
					continue	
				out.write(line)	
			f.close()
		if self.epgautodown.value == True:
			out.write(newcron)
		out.close()
		rc = system("crontab /etc/bhcron/bh.cron -c /etc/bhcron/")
		self.close()

#--------------------------------------- XMLTV EPG----------------------------------------------

class DeliteXmltepgProv(Screen):
	skin = """
	<screen position="339,150" size="602,400" title="Black Hole E2 EPG Settings">
		<widget name="lab1" position="20,10" size="240,30" font="Regular;20" transparent="1"/>
		<widget name="labprov" position="260,10" size="340,30" font="Regular;20"/>
		<widget name="lab1a" position="20,50" size="240,30" font="Regular;20" transparent="1"/>
		<widget name="labtype" position="260,50" size="340,30" font="Regular;20"/>
		<widget name="lab2" position="20,90" size="240,30" font="Regular;20" valign="center" transparent="1"/>
		<widget name="laburl" position="260,90" size="340,30" font="Regular;20" valign="center"/>
		<widget name="lab3" position="20,130" size="240,30" font="Regular;20" valign="center" transparent="1"/>
		<widget name="lablang" position="260,130" size="340,30" valign="center" font="Regular;20"/>
		<widget name="lab4" position="20,170" size="240,30" font="Regular;20" valign="center" transparent="1"/>
		<widget name="labmaxd" position="260,170" size="240,30" valign="center" font="Regular;20"/>
		<widget name="lsinactive" position="10,210" zPosition="1" pixmap="skin_default/icons/ninactive.png" size="32,32" alphatest="on"/>
		<widget name="lsactive" position="10,210" zPosition="2" pixmap="skin_default/icons/nactive.png" size="32,32" alphatest="on"/>
		<widget name="lab5" position="50,210" size="400,30" font="Regular;20" valign="center" transparent="1"/>
		<widget name="lab6" position="20,250" size="380,30" font="Regular;20" valign="center" transparent="1"/>
		<widget name="labtimes" position="430,250" size="60,30" font="Regular;20" valign="center" backgroundColor="black"/>
		<ePixmap pixmap="skin_default/buttons/red.png" position="40,350" size="140,40" alphatest="on"/>
		<widget name="key_red" position="45,350" zPosition="1" size="140,40" font="Regular;20" halign="center" valign="center" backgroundColor="#9f1313" transparent="1"/>
		<ePixmap pixmap="skin_default/buttons/green.png" position="220,350" size="140,40" alphatest="on" />
		<widget name="key_green" position="225,350" zPosition="1" size="140,40" font="Regular;20" halign="center" valign="center" backgroundColor="#1f771f" transparent="1"/>
		<ePixmap pixmap="skin_default/buttons/yellow.png" position="380,350" size="200,40" alphatest="on"/>
		<widget name="key_yellow" position="385,350" zPosition="1" size="200,40" font="Regular;20" halign="center" valign="center" backgroundColor="#a08500" transparent="1"/>
	</screen>"""
	
	def __init__(self, session, provider):
		Screen.__init__(self, session)
		
		self.provider = provider
		self["lab1"] = Label(_("Provider Name:"))
		self["labprov"] = Label("")
		self["lab1a"] = Label(_("Epg Type:"))
		self["labtype"] = Label("")
		self["lab2"] = Label(_("Url:"))
		self["laburl"] = Label("")
		self["lab3"] = Label("Lanugage:")
		self["lablang"] = Label("")
		self["lab4"] = Label("Max days to download:")
		self["labmaxd"] = Label("")
		self["lsinactive"] = Pixmap()
		self["lsactive"] = Pixmap()
		self["lab5"] = Label(_("Enable Automatic EPG Refresh"))
		self["lab6"] = Label(_("Refresh EPG every day at time:"))
		self["labtimes"] = Label("")
		self["key_red"] = Label(_("Settings"))
		self["key_green"] = Label(_("Channels"))
		self["key_yellow"] = Label(_("Download now"))
		
		self["actions"] = ActionMap(["WizardActions", "ColorActions"],
		{
			"back": self.close,
			"red": self.setupmyprov,
			"green": self.setchans,
			"yellow": self.downloadNow
		})

		self.onLayoutFinish.append(self.updatemyinfo)
		
	def updatemyinfo(self):
		self["lsinactive"].hide()
		self["lsactive"].hide()
		strview = ""
		mytmpt = "n/a"
		self["labprov"].setText(self.provider)
		
		parts = nab_Get_EpgProvider(self.provider)
		myurl = parts[2]
		self["labtype"].setText(parts[1])
		self["laburl"].setText(parts[2])
		self["labmaxd"].setText(parts[3])
		self["lablang"].setText(parts[4])
		
		if fileExists("/etc/bhcron/root"):
			f = open("/etc/bhcron/root",'r')
 			for line in f.readlines():
				if line.find(myurl) != -1:
					strview = line
					break
 			f.close()
		if strview:
			parts = strview.strip().split()
			mytmpt = parts[1] + ":" + parts[0]
			self["lsactive"].show()
		else:
			self["lsinactive"].show()
			
		self["labtimes"].setText(mytmpt)
		
	def downloadNow(self):
		self.session.open(DeliteDownEpgNow, self.provider)
		
		
	def setupmyprov(self):
		self.session.openWithCallback(self.updatemyinfo, DeliteXepgSetup, self.provider)
		
		
	def setchans(self):
		myfile = nab_Get_Channelsfile(self.provider)
		if myfile:
			self.session.open(DeliteEpgChannels, self.provider)
		else:
			self.session.open(MessageBox, "Sorry, Channel List not available for this Provider.", MessageBox.TYPE_INFO)
		
		
class DeliteXepgSetup(Screen, ConfigListScreen):
	skin = """
	<screen position="339,190" size="602,340" title="Black Hole E2 EPG Setup">
		<widget name="lab1" position="10,10" size="240,30" font="Regular;20" transparent="1"/>
		<widget name="labprov" position="260,10" size="340,30" font="Regular;20"/>
		<widget name="config" position="10,40" size="580,250" scrollbarMode="showOnDemand" />
		<ePixmap pixmap="skin_default/buttons/red.png" position="235,290" size="150,40" alphatest="on" />
		<widget name="key_red" position="235,290" zPosition="1" size="150,40" font="Regular;20" halign="center" valign="center" backgroundColor="#9f1313" transparent="1" />
	</screen>"""
	
	def __init__(self, session, provider):
		Screen.__init__(self, session)
		
		self.provider = provider
		self.list = []
		ConfigListScreen.__init__(self, self.list)
		self["key_red"] = Label(_("Save"))
		self["lab1"] = Label(_("Provider Name:"))
		self["labprov"] = Label(provider)
		self["actions"] = ActionMap(["WizardActions", "ColorActions"],
		{
			"red": self.saveMyprov,
			"back": self.close

		})
			
		self.updateList()
		

	def updateList(self):
	
		self.epgautodown = NoSave(ConfigYesNo(default=False))
		self.timerentry_starttime = NoSave(ConfigClock(default=0))
		self.maxdays = NoSave(ConfigSelection(default = "3", choices = [
		("1", "1"), ("2", "2"), ("3", "3"), ("4", "4"), ("5", "5"),
		("6", "6"), ("7", "7"), ("8", "8")]))
		
		strview = ""
		mytmpt = [23,20]
		autodown = False
		maxdays = "3"
		
		parts = nab_Get_EpgProvider(self.provider)
		myurl = parts[2]
		maxdays = parts[3]
		
		if fileExists("/etc/bhcron/root"):
			f = open("/etc/bhcron/root",'r')
 			for line in f.readlines():
				if line.find(myurl) != -1:
					strview = line
					break
 			f.close()
		
		if strview:
			parts = strview.strip().split()
			mytmpt = [int(parts[1]), int(parts[0])]
			autodown = True
		
		self.epgautodown.value = autodown
		self.timerentry_starttime.value = mytmpt
		self.maxdays.value = maxdays
		
		epg_autodown = getConfigListEntry(_("Enable Automatic EPG Refresh"), self.epgautodown)
		self.list.append(epg_autodown)
		starttime = getConfigListEntry(_("Refresh EPG every day at time"), self.timerentry_starttime)
		self.list.append(starttime)
		epg_maxdays = getConfigListEntry(_("Max days to download"), self.maxdays)
		self.list.append(epg_maxdays)
		
		self["config"].list = self.list
		self["config"].l.setList(self.list)		
	
	def saveMyprov(self):
		
		inme = open("/etc/Bhepgproviders.cfg",'r')
		out = open("/etc/Bhepgproviders.tmp",'w')
		for line in inme.readlines():
			parts = line.split(",")
			if parts[0] == self.provider:
				line = parts[0] + "," + parts[1] + "," + parts[2] + "," + self.maxdays.value + "," + parts[4]
			out.write(line)
		out.close()
		inme.close()
		os_rename("/etc/Bhepgproviders.tmp", "/etc/Bhepgproviders.cfg")	
			
		parts = nab_Get_EpgProvider(self.provider)
		url = parts[2]
		croncmd = "/usr/bin/Blackholecmd webxepg," + parts[2] + "," + parts[3] + "," + parts[4]
		hour = "%02d" % (self.timerentry_starttime.value[0])
		minutes =  "%02d" % (self.timerentry_starttime.value[1])
		newcron = minutes + " " + hour + " * * * " + croncmd + "\n"
		
		out = open("/etc/bhcron/bh.cron", "w")
		if fileExists("/etc/bhcron/root"):
			f = open("/etc/bhcron/root",'r')
			for line in f.readlines():
				if line.find(url) != -1:
					continue	
				out.write(line)	
			f.close()
		if self.epgautodown.value == True:
			out.write(newcron)
		out.close()
		rc = system("crontab /etc/bhcron/bh.cron -c /etc/bhcron/")
		self.close()
		

#--------------------------------------- CHANNELS PANEL----------------------------------------------

class DeliteEpgChannels(Screen, ConfigListScreen):
	skin = """
	<screen position="339,190" size="602,340" title="Epg Channels Setup">
		<widget name="config" position="30,10" size="540,275" scrollbarMode="showOnDemand"/>
		<widget name="Linconn" position="30,285" size="540,20" font="Regular;18" halign="center" valign="center" backgroundColor="#9f1313"/>
		<ePixmap pixmap="skin_default/buttons/red.png" position="50,300" size="140,40" alphatest="on"/>
		<ePixmap pixmap="skin_default/buttons/green.png" position="400,300" size="140,40" alphatest="on"/>
		<widget name="key_red" position="50,300" zPosition="1" size="140,40" font="Regular;20" halign="center" valign="center" backgroundColor="#9f1313" transparent="1"/>
		<widget name="key_green" position="420,300" zPosition="1" size="140,40" font="Regular;20" halign="center" valign="center" backgroundColor="#1f771f" transparent="1"/>
	</screen>"""


	def __init__(self, session, provider):
		Screen.__init__(self, session)
		
		self.provider = provider
		self.list = []
		ConfigListScreen.__init__(self, self.list)
		self["key_red"] = Label(_("Save"))
		self["key_green"] = Label(_("Update List"))
		self["Linconn"] = Label("Wait please download in progress ...")
		self["Linconn"].hide()
		
		self["actions"] = ActionMap(["WizardActions", "ColorActions"],
		{
			"red": self.saveMychans,
			"green": self.updateMychans,
			"back": self.close

		})
			
		self.updateList()
		
	
	def updateList(self):
		myfile = nab_Get_Channelsfile(self.provider)
	
		self.list = []
		if myfile and fileExists(myfile):
			f = open(myfile,'r')
			for line in f.readlines():
				parts = line.strip().split(';')
				if len(parts) > 1:
					item = NoSave(ConfigYesNo(default=False))
					item.value = False
					if parts[0] == '1':
						item.value = True
					text = parts[2]
					item2 = getConfigListEntry(text, item)
					self.list.append(item2)
				
			f.close()
			self["config"].list = self.list
			self["config"].l.setList(self.list)


	def saveMychans(self):
		myfile = nab_Get_Channelsfile(self.provider)
		chand = {}
		for x in self["config"].list:
			name = x[0]
			y = "0"
			if x[1].value == True:
				y = "1"
			chand[name] = y
			
		if fileExists(myfile):
			inme = open(myfile,'r')
			out = open("/usr/share/dict/channels.tmp",'w')
			for line in inme.readlines():
				parts = line.strip().split(';')
				if len(parts) > 1:
					text = parts[2]
					value = chand[text]
					line = value + line[1:]
					out.write(line)
		
			out.close()
			inme.close()
		
		if fileExists("/usr/share/dict/channels.tmp"):
			cmd = "mv -f  /usr/share/dict/channels.tmp " + myfile
			system(cmd)
			
		self.session.open(MessageBox, "Channels List Saved.", MessageBox.TYPE_INFO)
		self.close()
	
	def updateMychans(self):
		myfile = nab_Get_Channelsfile(self.provider)
#todo: update this list availablechans
		availablechans = ["/usr/share/dict/channels.it", "/usr/share/dict/channels.uk", "/usr/share/dict/channels.au"]
		if myfile in availablechans:
			self.session.openWithCallback(self.updateList, DeliteDownChannels, self.provider)
		else:
			self.session.open(MessageBox, "Sorry, function not available for this provider.", MessageBox.TYPE_INFO)

class DeliteDownChannels(Screen):
	skin = """
	<screen position="380,150" size="520,240" title="Update Channels List">
		<widget name="lab1" position="10,10" size="500,180" font="Regular;20" halign="center" valign="center" transparent="1"/>
		<ePixmap pixmap="skin_default/buttons/red.png" position="220,200" size="140,40" alphatest="on"/>
		<widget name="key_red" position="220,200" zPosition="1" size="140,40" font="Regular;20" halign="center" valign="center" backgroundColor="#9f1313" transparent="1"/>
	</screen>"""
	
	def __init__(self, session, provider):
		Screen.__init__(self, session)
		
		self.provider = provider
		msg = "Wait please," + provider + " Channels list download in progress..."
		self["lab1"] = Label(msg)
		self["key_red"] = Label(_("Close"))
		
		self["actions"] = ActionMap(["WizardActions", "ColorActions"],
		{
			"back": self.close,
			"red": self.close,
			"ok": self.close
		})
		self.activityTimer = eTimer()
		self.activityTimer.timeout.get().append(self.startdownload)
		self.oldpopconfig = config.misc.deliteepgpop.value
		self.oldchanref = None
		config.misc.deliteepgpop.value = False
		config.misc.deliteepgpop.save()
		self.onLayoutFinish.append(self.startShow)
		self.onClose.append(self.__onClose)
		
	def startShow(self):
		parts = nab_Get_EpgProvider(self.provider)
		self.oldchanref = self.session.nav.getCurrentlyPlayingServiceReference()
		chanref = parts[3]
		ref = eServiceReference(chanref)
		self.session.nav.playService(ref)
		self.activityTimer.start(3000)
		
	def startdownload(self):
		self.activityTimer.stop()		
#Todo: substitute this external command with integrated epgcache function
		if self.provider == "Sky-Ita":
			os_remove("/usr/share/dict/channels.it")
			cmd = "/usr/bin/getepgchannels -l it"
		elif self.provider == "Sky-Uk":
			os_remove("/usr/share/dict/channels.uk")
			cmd = "/usr/bin/getepgchannels -l uk"
		rc = system(cmd)
#Endo Todo
		self["lab1"].setText("Channels List Successfully Updated.")
		

	def __onClose(self):
		config.misc.deliteepgpop.value = self.oldpopconfig
		config.misc.deliteepgpop.save()
		if self.oldchanref:
			self.session.nav.playService(self.oldchanref)
		del self.activityTimer



#--------------------------------------- DOWNLOAD EPG----------------------------------------------

class DeliteDownEpgNow(Screen):
	skin = """
	<screen position="240,560" size="800,100" title="Black Hole Epg Download" flags="wfNoBorder">
		<widget name="lab1" position="10,10" size="780,40" font="Regular;22" halign="center" transparent="1"/>
		<ePixmap pixmap="skin_default/buttons/red.png" position="300,60" size="140,40" alphatest="on"/>
		<widget name="key_red" position="300,60" zPosition="1" size="140,40" font="Regular;20" halign="center" valign="center" backgroundColor="#9f1313" transparent="1"/>
	</screen>"""
	
	def __init__(self, session, provider):
		Screen.__init__(self, session)
		
		self.provider = provider
		msg = "Wait please for the Epg to complete, and press the red button to exit"
		self["lab1"] = Label(msg)
		self["key_red"] = Label(_("Close"))
		
		self["actions"] = ActionMap(["WizardActions", "ColorActions"],
		{
			"back": self.close,
			"red": self.close,
			"ok": self.close
		})
		self.activityTimer = eTimer()
		self.activityTimer.timeout.get().append(self.startdownload)
		self.oldpopconfig = config.misc.deliteepgpop.value
		self.oldchanref = None
		config.misc.deliteepgpop.value = True
		config.misc.deliteepgpop.save()
		self.onLayoutFinish.append(self.startShow)
		self.onClose.append(self.__onClose)
		
	def startShow(self):
		self.activityTimer.start(10)
		
	def startdownload(self):
		self.activityTimer.stop()
		
		parts = nab_Get_EpgProvider(self.provider)
		
		if parts[1] == "xmltv":
			self["lab1"].setText("Wait Please... Epg Download in progress....")
			provider = parts[2]
			maxdays = parts[3]
			language = parts[4]
			epgcache = eEPGCache.getInstance()
			ret = epgcache.readXmltv(('P',provider,maxdays,language));
			self["lab1"].setText("Epg Download complete. Press the red button to exit")
		elif parts[1] == "ext_dat":
			myurl = parts[2]
			myext = ""
			if myurl.find('.dat.gz') != -1:
				myext = ".gz"
			elif myurl.find('.dat.bz2') != -1:
				myext = ".bz2"
			else:
				self.session.open(MessageBox, "Wrong file format. Only bz2 and gzip files are allowed (.dat.gz .dat.bz2).", MessageBox.TYPE_ERROR)
				self.close()
			
			self["lab1"].hide()
			self["lab1"].setText("Wait Please... epg.dat file download in progress....")
			self["lab1"].show()
			myepgpath = config.misc.epgcache_filename.value
			
			myepgfile = myepgpath + myext
			
			try:
				filein = urlopen(myurl)
			except HTTPError, e:
    				self["lab1"].setText("Sorry, Connection Failed.")
			except URLError, e:
    				self["lab1"].setText("Sorry, Connection Failed.")
			else:
				fileout = open(myepgfile, "wb")
				while True:
					bytes = filein.read(1024000)
					fileout.write(bytes) 
					if bytes == "":
						break
				filein.close()
				fileout.close()
			
			if fileExists(myepgfile):
				cmd = "gunzip -f " + myepgfile
				if myext == ".bz2":
					cmd = "bunzip2 -f " + myepgfile
				rc = system(cmd)
				epgcache = eEPGCache.getInstance()
				epgcache.load()
				self["lab1"].hide()
				self["lab1"].setText("Saving epg.dat....")
				self["lab1"].show()
				epgcache.save()
				self["lab1"].setText("Epg Download complete. Press the red button to exit")
		else:
			self.oldchanref = self.session.nav.getCurrentlyPlayingServiceReference()
			chanref = parts[3]
			epgcache = eEPGCache.getInstance()
			ret = epgcache.Nab_reset_timer()
			ref = eServiceReference(chanref)
			self.session.nav.playService(ref)
			

	def __onClose(self):
		config.misc.deliteepgpop.value = self.oldpopconfig
		config.misc.deliteepgpop.save()
		if self.oldchanref:
			self.session.nav.playService(self.oldchanref)
		del self.activityTimer
		
	
	

