from Screens.Screen import Screen

from enigma import eTimer
from Screens.MessageBox import MessageBox
from Screens.VirtualKeyBoard import VirtualKeyBoard
from Components.ActionMap import ActionMap
from Components.Label import Label
from Components.ScrollLabel import ScrollLabel
from Components.Sources.List import List
from Components.Pixmap import Pixmap
from Components.ConfigList import ConfigListScreen
from Components.config import getConfigListEntry, config, ConfigText, ConfigNumber, NoSave
from Tools.LoadPixmap import LoadPixmap
from Tools.Directories import fileExists
from os import system
from BhUtils import nab_Read_CCCinfoCfg, nab_Write_CCCinfoCfg, DeliteGetSkinPath
from re import sub


class DeliteCCcMain(Screen):
	skin = """
	<screen position="160,100" size="390,360" title="Black Hole E2 CCcam Info">
		<widget source="list" render="Listbox" position="20,15" size="350,320" scrollbarMode="showOnDemand" >
			<convert type="TemplatedMultiContent">
                	{"template": [
                	MultiContentEntryText(pos = (50, 1), size = (300, 36), flags = RT_HALIGN_LEFT|RT_VALIGN_CENTER, text = 0),
                	MultiContentEntryPixmapAlphaTest(pos = (4, 2), size = (34, 34), png = 1),
                	],
                	"fonts": [gFont("Regular", 24)],
                	"itemHeight": 36
                	}
            		</convert>
		</widget>
		<widget name="Linconn" position="0,325" size="390,35" font="Regular;20" halign="center" valign="center" backgroundColor="#9f1313" />
	</screen>"""
	
	def __init__(self, session):
		
		Screen.__init__(self, session)

		self.list = []
		self["list"] = List(self.list)
		self.updateList()
		
		self["Linconn"] = Label("Wait please connection to CCcam in progress ...")
		self["Linconn"].hide()
		
		self["actions"] = ActionMap(["WizardActions", "ColorActions"],
		{
			"ok": self.KeyOk,
			"back": self.close

		})
		
	def updateList(self):
		
		self.list = [ ]
		
		mypath = DeliteGetSkinPath()
		
		mypixmap = mypath + "icons/ccc_home.png"
		png = LoadPixmap(mypixmap)
		name = "Main"
		idx = 0
		res = (name, png, idx)
		self.list.append(res)
		
		mypixmap = mypath + "icons/ccc_activeclients.png"
		png = LoadPixmap(mypixmap)
		name = "Active Clients"
		idx = 1
		res = (name, png, idx)
		self.list.append(res)
		
		mypixmap = mypath + "icons/ccc_clients.png"
		png = LoadPixmap(mypixmap)
		name = "Clients"
		idx = 2
		res = (name, png, idx)
		self.list.append(res)
		
		mypixmap = mypath + "icons/ccc_servers.png"
		png = LoadPixmap(mypixmap)
		name = "Servers"
		idx = 3
		res = (name, png, idx)
		self.list.append(res)
		
		mypixmap = mypath + "icons/ccc_shares.png"
		png = LoadPixmap(mypixmap)
		name = "Shares"
		idx = 4
		res = (name, png, idx)
		self.list.append(res)
		
		mypixmap = mypath + "icons/ccc_providers.png"
		png = LoadPixmap(mypixmap)
		name = "Providers"
		idx = 5
		res = (name, png, idx)
		self.list.append(res)
		
		mypixmap = mypath + "icons/ccc_entitlements.png"
		png = LoadPixmap(mypixmap)
		name = "Entitlements"
		idx = 6
		res = (name, png, idx)
		self.list.append(res)
		
		mypixmap = mypath + "icons/ccc_setup.png"
		png = LoadPixmap(mypixmap)
		name = "Setup"
		idx = 7
		res = (name, png, idx)
		self.list.append(res)
		
		self["list"].list = self.list
	
	
	def KeyOk(self):
		self.sel = self["list"].getCurrent()
		if self.sel:
			self.sel = self.sel[2]
			
		if self.sel == 0:
			self.session.open(DeliteCCcHo)
		elif self.sel == 1:
			self.session.open(DeliteCCcAc)
		elif self.sel == 2:
			self.session.open(DeliteCCcCl)
		elif self.sel == 3:
			self.session.open(DeliteCCcSe)
		elif self.sel == 4:
			self.session.open(DeliteCCcSh)
		elif self.sel == 5:
			self.session.open(DeliteCCcPr)
		elif self.sel == 6:
			self.session.open(DeliteCCcEnt)
		elif self.sel == 7:
			self.session.open(DeliteCCcSetup)



class DeliteCCcSetup(Screen, ConfigListScreen):
	skin = """
	<screen position="140,140" size="440,340" title="Black Hole E2 CCcam Info Setup">
		<widget name="lab1" position="10,10" size="420,120" font="Regular;18" valign="center" transparent="1"/>
		<widget name="config" position="10,130" size="420,120" scrollbarMode="showOnDemand" />
		<ePixmap pixmap="skin_default/buttons/red.png" position="150,290" size="140,40" alphatest="on" />
		<widget name="key_red" position="150,290" zPosition="1" size="140,40" font="Regular;20" halign="center" valign="center" backgroundColor="#9f1313" transparent="1" />
	</screen>"""
	
	def __init__(self, session):
		Screen.__init__(self, session)
		
		self.list = []
		self["lab1"] = Label("You can connect to your local CCcam or to a remote box. Use the address: 127.0.0.1 for local connections.\n________________________________________")
		ConfigListScreen.__init__(self, self.list)
		self["key_red"] = Label(_("Save"))
		
		
		self["actions"] = ActionMap(["WizardActions", "ColorActions"],
		{
			"red": self.saveMyccc,
			"back": self.close,
			"green": self.vkeyb

		})
			
		self.updateList()
	
	
	def updateList(self):
	
		self.ccc_host = NoSave(ConfigText(fixed_size = False, default="127.0.0.1"))
		self.ccc_user = NoSave(ConfigText(fixed_size = False))
		self.ccc_pass = NoSave(ConfigText(fixed_size = False))
		self.ccc_port = NoSave(ConfigNumber(default=16001))
		
		mycfg = nab_Read_CCCinfoCfg()
		self.ccc_host.value = mycfg[0]
		self.ccc_user.value = mycfg[1]
		self.ccc_pass.value = mycfg[2]
		self.ccc_port.value = int(mycfg[3])
		
		ccc_host1 = getConfigListEntry("Host", self.ccc_host)
		self.list.append(ccc_host1)
		
		ccc_user1 = getConfigListEntry("Webinfo Username", self.ccc_user)
		self.list.append(ccc_user1)
		
		ccc_pass1 = getConfigListEntry("Webinfo Password", self.ccc_pass)
		self.list.append(ccc_pass1)
		
		ccc_port1 = getConfigListEntry("Webinfo Port", self.ccc_port)
		self.list.append(ccc_port1)
		
		self["config"].list = self.list
		self["config"].l.setList(self.list)
		
		
	def vkeyb(self):
		sel = self["config"].getCurrent()
		if sel:
			self.vkvar = sel[0]
			value = "xmeo"
			if self.vkvar == "Webinfo Username":
				value = self.ccc_user.value
			elif self.vkvar == "Webinfo Password":
				value = self.ccc_pass.value
			
			
			if value != "xmeo":
				self.session.openWithCallback(self.UpdateAgain, VirtualKeyBoard, title=self.vkvar, text=value)
			else:
				self.session.open(MessageBox, "Please use Virtual Keyboard for text rows only:\n-Webinfo Username\n-Webinfo Password", MessageBox.TYPE_INFO)
	
	def UpdateAgain(self, newt):
		self.list = [ ]
		if newt is None:
			newt = ""
		if newt.strip() != "":
			if self.vkvar == "Webinfo Username":
				self.ccc_user.value = newt
			elif self.vkvar == "Webinfo Password":
				self.ccc_pass.value = newt
	
			ccc_host1 = getConfigListEntry("Host", self.ccc_host)
			self.list.append(ccc_host1)
			ccc_user1 = getConfigListEntry("Webinfo Username", self.ccc_user)
			self.list.append(ccc_user1)
			ccc_pass1 = getConfigListEntry("Webinfo Password", self.ccc_pass)
			self.list.append(ccc_pass1)
			ccc_port1 = getConfigListEntry("Webinfo Port", self.ccc_port)
			self.list.append(ccc_port1)
		
			self["config"].list = self.list
			self["config"].l.setList(self.list)
			#self.session.open(MessageBox, "aggiornata", MessageBox.TYPE_INFO)
	
		
	def saveMyccc(self):
		myhost = self.ccc_host.value.strip()
		myuser = self.ccc_user.value.strip()
		mypass = self.ccc_pass.value.strip()
		myport = str(self.ccc_port.value)
		
		mycfg = [myhost, myuser, mypass, myport]
		nab_Write_CCCinfoCfg(mycfg)
		mybox = self.session.open(MessageBox, "Configuration saved.", MessageBox.TYPE_INFO)
		mybox.setTitle("Info")
		self.close()
		
				

class DeliteCCcHo(Screen):
	skin = """
	<screen position="80,95" size="560,400" title="Black Hole Cccam Main Info">
		<widget name="infotext" position="10,10" size="540,340" font="Regular;20" />
		<widget name="Linconn" position="0,360" size="560,35" font="Regular;20" halign="center" valign="center" backgroundColor="#9f1313" />
	</screen>"""
	
	def __init__(self, session):
		Screen.__init__(self, session)

		self["infotext"] = ScrollLabel()
		self["Linconn"] = Label("Wait please, while CCcam reply ....")
		self["actions"] = ActionMap(["WizardActions"],
		{
			"ok": self.close,
			"back": self.close,
			"up": self["infotext"].pageUp,
			"down": self["infotext"].pageDown

		})		
		
		self.activityTimer = eTimer()
		self.activityTimer.timeout.get().append(self.CCCconn)
		self.activityTimer.start(1, False)
		self.onClose.append(self.delTimer)
		
		
	def delTimer(self):
		del self.activityTimer
		
	def CCCconn(self):
		self.activityTimer.stop()
		mycfg = nab_Read_CCCinfoCfg()
		url = mycfg[4]
		cmd = "wget -O /tmp/cpanel.tmp " + url
		rc = system(cmd)
		strview = ""
		if fileExists("/tmp/cpanel.tmp"):
			f = open("/tmp/cpanel.tmp",'r')
 			for line in f.readlines():
				line = line.replace('\n', '')
				line = line.replace('<BR>', '\n')
				line = sub('<br(\s+/)?>', '\n', line)
				line = sub('<(.*?)>', '', line)
				strview += line
		
 			f.close()
			system("rm -f /tmp/cpanel.tmp")
		else:
			mybox = self.session.open(MessageBox, "Sorry. Connection to CCcam refused.\nCheck that CCcam is running and your webinfo settings.", MessageBox.TYPE_INFO)
			mybox.setTitle("Info")
		self["Linconn"].hide()
		strview = strview.replace('CCcam info pages', '')
		self["infotext"].setText(strview)
		
class DeliteCCcEnt(Screen):
	skin = """
	<screen position="80,95" size="560,400" title="Black Hole Cccam Entitlements Info">
		<widget name="infotext" position="10,10" size="540,340" font="Regular;20" />
		<widget name="Linconn" position="0,360" size="560,35" font="Regular;20" halign="center" valign="center" backgroundColor="#9f1313" />
	</screen>"""
	
	def __init__(self, session):
		Screen.__init__(self, session)

		self["infotext"] = ScrollLabel()
		self["Linconn"] = Label("Wait please, while CCcam reply ....")
		self["actions"] = ActionMap(["WizardActions"],
		{
			"ok": self.close,
			"back": self.close,
			"up": self["infotext"].pageUp,
			"down": self["infotext"].pageDown

		})		
		
		self.activityTimer = eTimer()
		self.activityTimer.timeout.get().append(self.CCCconn)
		self.activityTimer.start(1, False)
		self.onClose.append(self.delTimer)
		
	def delTimer(self):
		del self.activityTimer
		
	def CCCconn(self):
		self.activityTimer.stop()
		mycfg = nab_Read_CCCinfoCfg()
		url = mycfg[4]
		url += "/entitlements"
		cmd = "wget -O /tmp/cpanel.tmp " + url
		rc = system(cmd)
		strview = ""
		if fileExists("/tmp/cpanel.tmp"):
			f = open("/tmp/cpanel.tmp",'r')
 			for line in f.readlines():
				line = line.replace('<BR>', '\n')
				line = sub('<br(\s+/)?>', '\n', line)
				line = sub('<(.*?)>', '', line)
				strview += line
		
 			f.close()
			system("rm -f /tmp/cpanel.tmp")
		else:
			mybox = self.session.open(MessageBox, "Sorry. Connection to CCcam refused.\nCheck that CCcam is running and your webinfo settings.", MessageBox.TYPE_INFO)
			mybox.setTitle("Info")
		self["Linconn"].hide()
		strview = strview.replace('CCcam info pages', '')
		strview = strview.replace('server ', 'server\n\n')
		self["infotext"].setText(strview)
		#self.setTitle("ciao")
		
class DeliteCCcAc(Screen):
	skin = """
	<screen position="80,95" size="560,400" title="Active Clients">
		<widget source="list" render="Listbox" position="10,10" size="540,270" scrollbarMode="showOnDemand" >
			<convert type="StringList" />
		</widget>
		<widget name="statuslab" position="10,290" size="540,70" font="Regular;16" valign="center" backgroundColor="#333f3f3f" foregroundColor="#FFC000" shadowOffset="-2,-2" shadowColor="black" />
		<widget name="Linconn" position="10,360" size="540,35" font="Regular;20" halign="center" valign="center" backgroundColor="#9f1313" />
	</screen>"""
	
	def __init__(self, session):
		Screen.__init__(self, session)

		self.list = []
		self["list"] = List(self.list)
		self["list"].onSelectionChanged.append(self.schanged)
		self["statuslab"] = Label("")
		self["Linconn"] = Label("Wait please, while CCcam reply ....")
		self["actions"] = ActionMap(["WizardActions"],
		{
			"ok": self.close,
			"back": self.close,

		})		
		
		self.activityTimer = eTimer()
		self.activityTimer.timeout.get().append(self.CCCconn)
		self.activityTimer.start(1, False)
		self.onClose.append(self.delTimer)
	
	def delTimer(self):
		del self.activityTimer
		
	def CCCconn(self):
		self.activityTimer.stop()
		mycfg = nab_Read_CCCinfoCfg()
		url = mycfg[4]
		url += "/activeclients"
		cmd = "wget -O /tmp/cpanel.tmp " + url
		rc = system(cmd)
		strview = ""
		mytitle = "Active Clients"
		if fileExists("/tmp/cpanel.tmp"):
			f = open("/tmp/cpanel.tmp",'r')
			check = 0
			mykey = 0
 			for line in f.readlines():
				if check == 0:
					if line.find('20 SECONDS') != -1:
						parts = line.strip().split()
						mytitle ="Active clients in last 20 seconds [" + parts[0] + " online]"
						check = 1
				elif check == 1:
					if line.find('Last used share') != -1:
						check = 2
				elif check == 2:
					check = 3
				elif check == 3:
					if line.find('+') == 0:
						break
					parts = line.strip().split("|")
					key = parts[1].strip()
					mytxt = key + " - " + parts[2]
					res = (mytxt, line)
					self.list.append(res)
					mykey = mykey + 1
		
 			f.close()
			system("rm -f /tmp/cpanel.tmp")
			self["list"].list = self.list
			self.setTitle(mytitle)
			self.schanged()
		else:
			mybox = self.session.open(MessageBox, "Sorry. Connection to CCcam refused.\nCheck that CCcam is running and your webinfo settings.", MessageBox.TYPE_INFO)
			mybox.setTitle("Info")

		self["Linconn"].hide()
		
		
	def schanged(self):
		mysel = self["list"].getCurrent()
		if mysel:
			mytext = mysel[1]
			parts = mytext.split("|")
			ct = parts[3]
			it = parts[4] 
		
			mytext = "Connected time: " + ct[4:] + "\t" + "Idle Time: " + it[4:] + "\nEcm: " + parts[5] + "\tEmm:" + parts[6] + "\tVersion: " + parts[7] + "\nLast share: " + parts[8]
			self["statuslab"].setText(mytext)
			
		
class DeliteCCcCl(Screen):
	skin = """
	<screen position="80,95" size="560,400" title="Clients">
		<widget source="list" render="Listbox" position="10,10" size="540,270" scrollbarMode="showOnDemand" >
			<convert type="StringList" />
		</widget>
		<widget name="statuslab" position="10,290" size="540,70" font="Regular;16" valign="center" backgroundColor="#333f3f3f" foregroundColor="#FFC000" shadowOffset="-2,-2" shadowColor="black" />
		<widget name="Linconn" position="10,360" size="540,35" font="Regular;20" halign="center" valign="center" backgroundColor="#9f1313" />
	</screen>"""
	
	def __init__(self, session):
		Screen.__init__(self, session)

		self.list = []
		self["list"] = List(self.list)
		self["list"].onSelectionChanged.append(self.schanged)
		self["statuslab"] = Label("")
		self["Linconn"] = Label("Wait please, while CCcam reply ....")
		self["actions"] = ActionMap(["WizardActions"],
		{
			"ok": self.close,
			"back": self.close,

		})		
		
		self.activityTimer = eTimer()
		self.activityTimer.timeout.get().append(self.CCCconn)
		self.activityTimer.start(1, False)
		self.onClose.append(self.delTimer)
		
	def delTimer(self):
		del self.activityTimer
		
	def CCCconn(self):
		self.activityTimer.stop()
		mycfg = nab_Read_CCCinfoCfg()
		url = mycfg[4]
		url += "/clients"
		cmd = "wget -O /tmp/cpanel.tmp " + url
		rc = system(cmd)
		strview = ""
		mytitle = "Clients"
		if fileExists("/tmp/cpanel.tmp"):
			f = open("/tmp/cpanel.tmp",'r')
			check = 0
			mykey = 0
 			for line in f.readlines():
				if check == 0:
					if line.find('Connected clients:') != -1:
						pos = line.find('Connected clients:') + 18
						mytitle ="Connected Clients [" + line[pos:].strip() + " online]"
						check = 1
				elif check == 1:
					if line.find('Last used share') != -1:
						check = 2
				elif check == 2:
					check = 3
				elif check == 3:
					if line.find('+') == 0:
						break
					parts = line.strip().split("|")
					key = parts[1].strip()
					mytxt = key + " - " + parts[2]
					res = (mytxt, line)
					self.list.append(res)
					mykey = mykey + 1
		
 			f.close()
			system("rm -f /tmp/cpanel.tmp")
			self["list"].list = self.list
			self.setTitle(mytitle)
			self.schanged()
		else:
			mybox = self.session.open(MessageBox, "Sorry. Connection to CCcam refused.\nCheck that CCcam is running and your webinfo settings.", MessageBox.TYPE_INFO)
			mybox.setTitle("Info")

		self["Linconn"].hide()
		
		
	def schanged(self):
		mysel = self["list"].getCurrent()
		if mysel:
			mytext = mysel[1]
			parts = mytext.split("|")
			ct = parts[3]
			it = parts[4] 
		
			mytext = "Connected time: " + ct[4:] + "\t" + "Idle Time: " + it[4:] + "\nEcm: " + parts[5] + "\tEmm:" + parts[6] + "\tVersion: " + parts[7] + "\nLast share: " + parts[8]
			self["statuslab"].setText(mytext)
			

class DeliteCCcSe(Screen):
	skin = """
	<screen position="80,95" size="560,400" title="Servers">
		<widget source="list" render="Listbox" position="10,10" size="540,270" scrollbarMode="showOnDemand" >
			<convert type="TemplatedMultiContent">
                	{"template": [
                	MultiContentEntryText(pos = (40, 1), size = (500, 36), flags = RT_HALIGN_LEFT|RT_VALIGN_CENTER, text = 0),
                	MultiContentEntryPixmapAlphaTest(pos = (4, 2), size = (34, 34), png = 1),
                	],
                	"fonts": [gFont("Regular", 24)],
                	"itemHeight": 36
                	}
            		</convert>
		</widget>
		<widget name="statuslab" position="10,290" size="540,70" font="Regular;16" valign="center" backgroundColor="#333f3f3f" foregroundColor="#FFC000" shadowOffset="-2,-2" shadowColor="black" />
		<widget name="Linconn" position="10,360" size="540,35" font="Regular;20" halign="center" valign="center" backgroundColor="#9f1313" />
	</screen>"""
	
	def __init__(self, session):
		Screen.__init__(self, session)

		self.list = []
		self["list"] = List(self.list)
		self["list"].onSelectionChanged.append(self.schanged)
		self["statuslab"] = Label("")
		self["Linconn"] = Label("Wait please, while CCcam reply ....")
		self["actions"] = ActionMap(["WizardActions"],
		{
			"ok": self.close,
			"back": self.close,

		})		
		
		self.activityTimer = eTimer()
		self.activityTimer.timeout.get().append(self.CCCconn)
		self.activityTimer.start(1, False)
		self.onClose.append(self.delTimer)
		
	def delTimer(self):
		del self.activityTimer
		
	def CCCconn(self):
		self.activityTimer.stop()
		mycfg = nab_Read_CCCinfoCfg()
		url = mycfg[4]
		url += "/servers"
		cmd = "wget -O /tmp/cpanel.tmp " + url
		rc = system(cmd)
		strview = ""
		mytitle = "Servers"
		self.itemdesc = {}
		if fileExists("/tmp/cpanel.tmp"):
			f = open("/tmp/cpanel.tmp",'r')
			check = 0
			count = 0
			mykey = 0
 			for line in f.readlines():
				if check == 0:
					if line.find('Server connections:') != -1:
						check = 1
				elif check == 1:
					if line.find('CAID/Idents') != -1:
						check = 2
				elif check == 2:
					check = 3
				elif check == 3:
					if line.find('+') == 0:
						break
					parts = line.strip().split("|")
					key = parts[1].strip()
					if key:
						mytxt = key + " - " + parts[6].strip() + " Cards"
						isconn = parts[2].strip()
						mypixmap = "/usr/share/enigma2/skin_default/buttons/button_red.png"
						if isconn:
							mypixmap = "/usr/share/enigma2/skin_default/buttons/button_green.png"
							count = count + 1
						png = LoadPixmap(mypixmap)
						res = (mytxt, png, line)
						self.list.append(res)
						mykey = mykey + 1
		
 			f.close()
			system("rm -f /tmp/cpanel.tmp")
			self["list"].list = self.list
			mytitle ="Connected Servers [" + str(count) + " online]"
			self.setTitle(mytitle)
			self.schanged()
		else:
			mybox = self.session.open(MessageBox, "Sorry. Connection to CCcam refused.\nCheck that CCcam is running and your webinfo settings.", MessageBox.TYPE_INFO)
			mybox.setTitle("Info")

		self["Linconn"].hide()
		
		
	def schanged(self):
		mysel = self["list"].getCurrent()
		if mysel:
			mytext = mysel[2]
			parts = mytext.split("|")
			conn = parts[2].strip()
			typ = parts[3].strip()
			ver = parts[4].strip()
			nod = parts[5].strip()
			caid = parts[7].strip()
		
			mytext = "Uptime: " + conn + "\t" + "Type: " + typ + "\nVersion: " + ver + "\t\tNodeId:" + nod + "\nCaId: " + caid
			self["statuslab"].setText(mytext)
		
			
class DeliteCCcSh(Screen):
	skin = """
	<screen position="80,95" size="560,400" title="Shares">
		<widget source="list" render="Listbox" position="10,10" size="540,270" scrollbarMode="showOnDemand" >
			<convert type="StringList" />
		</widget>
		<widget name="statuslab" position="10,290" size="540,70" font="Regular;16" valign="center" backgroundColor="#333f3f3f" foregroundColor="#FFC000" shadowOffset="-2,-2" shadowColor="black" />
		<widget name="Linconn" position="10,360" size="540,35" font="Regular;20" halign="center" valign="center" backgroundColor="#9f1313" />
	</screen>"""
	
	def __init__(self, session):
		Screen.__init__(self, session)

		self.list = []
		self["list"] = List(self.list)
		self["list"].onSelectionChanged.append(self.schanged)
		self["statuslab"] = Label("")
		self["Linconn"] = Label("Wait please, while CCcam reply ....")
		self["actions"] = ActionMap(["WizardActions"],
		{
			"ok": self.close,
			"back": self.close,

		})		
		
		self.activityTimer = eTimer()
		self.activityTimer.timeout.get().append(self.CCCconn)
		self.activityTimer.start(1, False)
		self.onClose.append(self.delTimer)
	
	def delTimer(self):
		del self.activityTimer
		
	def CCCconn(self):
		self.activityTimer.stop()
		mycfg = nab_Read_CCCinfoCfg()
		url = mycfg[4]
		url += "/shares"
		cmd = "wget -O /tmp/cpanel.tmp " + url
		rc = system(cmd)
		strview = ""
		mytitle = "Shares"
		count = 0
		if fileExists("/tmp/cpanel.tmp"):
			f = open("/tmp/cpanel.tmp",'r')
			check = 0
 			for line in f.readlines():
				if check == 0:
					if line.find('Available shares:') != -1:
						pos = line.find('Available shares:') + 17
						mytitle ="Shares [" + line[pos:].strip() + " online]"
						check = 1
				elif check == 1:
					if line.find('Maxdown') != -1:
						check = 2
				elif check == 2:
					check = 3
				elif check == 3:
					if line.find('+') == 0:
						break
					parts = line.strip().split("|")
					key = parts[1].strip()
					mytxt = key + " CaId: " + parts[3].strip() + " Sys: " + parts[4].strip()
					mytxt2 = parts[2] + "|" + parts[5] + "|" +  parts[6] + "|" + parts[7]
					res = (mytxt, mytxt2)
					self.list.append(res)
					count = count + 1
 			f.close()
			system("rm -f /tmp/cpanel.tmp")
			self["list"].list = self.list
			self.setTitle(mytitle)
			self.schanged()
		else:
			mybox = self.session.open(MessageBox, "Sorry. Connection to CCcam refused.\nCheck that CCcam is running and your webinfo settings.", MessageBox.TYPE_INFO)
			mybox.setTitle("Info")

		self["Linconn"].hide()
		
		
	def schanged(self):
		mysel = self["list"].getCurrent()
		if mysel:
			mytext = mysel[1]
			parts = mytext.split("|")
			typ = parts[0].strip()
			prov = parts[1].strip()
			up = parts[2].strip()
			nod = parts[3].strip()
		
			mytext = "Type: " + typ + "\t" + "Providers: " + prov + "\nUphops MaxDown: " + up + "\nNodes: " + nod
			self["statuslab"].setText(mytext)			
			
class DeliteCCcPr(Screen):
	skin = """
	<screen position="80,95" size="560,400" title="Providers">
		<widget source="list" render="Listbox" position="10,10" size="540,270" scrollbarMode="showOnDemand" >
			<convert type="StringList" />
		</widget>
		<widget name="statuslab" position="10,290" size="540,70" font="Regular;16" valign="center" backgroundColor="#333f3f3f" foregroundColor="#FFC000" shadowOffset="-2,-2" shadowColor="black" />
		<widget name="Linconn" position="10,360" size="540,35" font="Regular;20" halign="center" valign="center" backgroundColor="#9f1313" />
	</screen>"""
	
	def __init__(self, session):
		Screen.__init__(self, session)

		self.list = []
		self["list"] = List(self.list)
		self["list"].onSelectionChanged.append(self.schanged)
		self["statuslab"] = Label("")
		self["Linconn"] = Label("Wait please, while CCcam reply ....")
		self["actions"] = ActionMap(["WizardActions"],
		{
			"ok": self.close,
			"back": self.close,

		})		
		
		self.activityTimer = eTimer()
		self.activityTimer.timeout.get().append(self.CCCconn)
		self.activityTimer.start(1, False)
		self.onClose.append(self.delTimer)
		
	def delTimer(self):
		del self.activityTimer
		
	def CCCconn(self):
		self.activityTimer.stop()
		mycfg = nab_Read_CCCinfoCfg()
		url = mycfg[4]
		url += "/providers"
		cmd = "wget -O /tmp/cpanel.tmp " + url
		rc = system(cmd)
		strview = ""
		mytitle = "Providers"
		if fileExists("/tmp/cpanel.tmp"):
			f = open("/tmp/cpanel.tmp",'r')
			count = 0
			check = 0
			mykey = 0
 			for line in f.readlines():
				if check == 0:
					if line.find('Available providers:') != -1:
						check = 1
				elif check == 1:
					if line.find('System') != -1:
						check = 2
				elif check == 2:
					check = 3
				elif check == 3:
					if line.find('+') == 0:
						break
					parts = line.strip().split("|")
					key = parts[3].strip()
					res = (key, line)
					self.list.append(res)
					mykey = mykey + 1
					count = count + 1
 			f.close()
			system("rm -f /tmp/cpanel.tmp")
			self["list"].list = self.list
			mytitle = "Available Providers : [" + str(count) + "]"
			self.setTitle(mytitle)
			self.schanged()
		else:
			mybox = self.session.open(MessageBox, "Sorry. Connection to CCcam refused.\nCheck that CCcam is running and your webinfo settings.", MessageBox.TYPE_INFO)
			mybox.setTitle("Info")

		self["Linconn"].hide()
		
		
	def schanged(self):
		mysel = self["list"].getCurrent()
		if mysel:
			mytext = mysel[1]
			parts = mytext.split("|")
			caid = parts[1].strip()
			prov = parts[2].strip()
			syst = parts[4].strip()
		
			mytext = "CaId: " + caid + "\n" + "Provider: " + prov + "\nSystem " + syst
			self["statuslab"].setText(mytext)
			
