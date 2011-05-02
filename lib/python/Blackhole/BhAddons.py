from Screens.Screen import Screen

from Screens.MessageBox import MessageBox
from Screens.Console import Console
from enigma import eTimer, loadPic
from Components.ActionMap import ActionMap
from Components.Label import Label
from Components.ScrollLabel import ScrollLabel
from Components.Sources.List import List
from Components.Pixmap import Pixmap, MultiPixmap
from Tools.LoadPixmap import LoadPixmap
from Tools.Directories import fileExists, pathExists, createDir
from os import system, listdir, chdir, getcwd, remove as os_remove
from urllib2 import Request, urlopen, URLError, HTTPError
from BhUtils import nab_strip_html, DeliteGetSkinPath


class DeliteAddons(Screen):
	skin = """
	<screen position="160,115" size="390,330" title="Black Hole E2 Addons Manager">
		<widget source="list" render="Listbox" position="10,16" size="370,300" scrollbarMode="showOnDemand" >
			<convert type="TemplatedMultiContent">
                	{"template": [
                    	MultiContentEntryText(pos = (50, 1), size = (320, 36), flags = RT_HALIGN_LEFT|RT_VALIGN_CENTER, text = 0),
                 	MultiContentEntryPixmapAlphaTest(pos = (4, 2), size = (36, 36), png = 1),
                    	],
                    	"fonts": [gFont("Regular", 22)],
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
		
		if (not pathExists("/var/uninstall")):
			createDir("/var/uninstall")
		
		self["actions"] = ActionMap(["WizardActions", "ColorActions"],
		{
			"ok": self.KeyOk,
			"back": self.close,

		})
		
	def updateList(self):
		self.list = [ ]
		mypath = DeliteGetSkinPath()
		
		mypixmap = mypath + "icons/addons_manager.png"
		png = LoadPixmap(mypixmap)
		name = "Addons Download Manager"
		idx = 0
		res = (name, png, idx)
		self.list.append(res)

		mypixmap = mypath + "icons/nabpackpanel.png"
		png = LoadPixmap(mypixmap)
		name = "Manual Install Bh packges"
		idx = 1
		res = (name, png, idx)
		self.list.append(res)
		
		mypixmap = mypath + "icons/ipkpackpanel.png"
		png = LoadPixmap(mypixmap)
		name = "Manual Install Ipk packges"
		idx = 2
		res = (name, png, idx)
		self.list.append(res)
		
		mypixmap = mypath + "icons/uninstpanel.png"
		png = LoadPixmap(mypixmap)
		name = "Addons Uninstall Panel"
		idx = 3
		res = (name, png, idx)
		self.list.append(res)
		
		mypixmap = mypath + "icons/statpanel.png"
		png = LoadPixmap(mypixmap)
		name = "Black Hole Statistics"
		idx = 4
		res = (name, png, idx)
		self.list.append(res)
		
		self["list"].list = self.list
		
	def KeyOk(self):
		
		self.sel = self["list"].getCurrent()
		if self.sel:
			self.sel = self.sel[2]
		
		if self.sel == 0:
			self.session.open(Nab_downArea)
		elif self.sel == 1:
			self.checkPanel()
		elif self.sel == 2:
			self.checkPanel2()
		elif self.sel == 3:
			self.session.open(Nab_uninstPanel)
		elif self.sel == 4:
			staturl = "http://www.vuplus-community.net/bhaddons/index.php?op=outmestats2"
			downfile = "/tmp/cpanel.tmp"
			if fileExists(downfile):
				os_remove(downfile)
			self.session.openWithCallback(self.StatsDone, Nab_ConnectPop, staturl, downfile)
		else:
			nobox = self.session.open(MessageBox, "Function Not Yet Available", MessageBox.TYPE_INFO)
			nobox.setTitle(_("Info"))
			
	def StatsDone(self):
		downfile = "/tmp/cpanel.tmp"	
		if fileExists(downfile):
			self.session.open(Nab_Stats)
		else:
			nobox = self.session.open(MessageBox, "Sorry, Connection Failed.", MessageBox.TYPE_INFO)
	
	def checkPanel(self):
		check = 0
		pkgs = listdir("/tmp")
		for fil in pkgs:
			if fil.find('.tgz') != -1:
				check = 1
		if check == 1:
			self.session.open(Nab_downPanel)
		else:
			mybox = self.session.open(MessageBox, "Nothing to install.\nYou have to Upload a bh.tgz package in the /tmp directory before to install Addons", MessageBox.TYPE_INFO)
			mybox.setTitle(_("Info"))
			
	def checkPanel2(self):
		check = 0
		pkgs = listdir("/tmp")
		for fil in pkgs:
			if fil.find('.ipk') != -1:
				check = 1
		if check == 1:
			self.session.open(Nab_downPanelIPK)
		else:
			mybox = self.session.open(MessageBox, "Nothing to install.\nYou have to Upload an ipk package in the /tmp directory before to install Addons", MessageBox.TYPE_INFO)
			mybox.setTitle(_("Info"))
		
class Nab_downArea(Screen):
	skin = """
	<screen position="160,115" size="390,330" title="Black Hole E2 Downloads Manager">
		<widget source="list" render="Listbox" position="10,15" size="370,280" scrollbarMode="showOnDemand" >
			<convert type="TemplatedMultiContent">
                	{"template": [
                   	MultiContentEntryText(pos = (50, 1), size = (320, 36), flags = RT_HALIGN_LEFT|RT_VALIGN_CENTER, text = 0),
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
		
		if (not pathExists("/var/uninstall")):
			createDir("/var/uninstall")
		
		self["actions"] = ActionMap(["WizardActions", "ColorActions"],
		{
			"ok": self.KeyOk,
			"back": self.close

		})
		
	def updateList(self):
		
		self.list = [ ]
		mypath = DeliteGetSkinPath()
		
		
		mypixmap = mypath + "icons/nabplugins.png"
		png = LoadPixmap(mypixmap)
		name = "Black Hole E2 Image Plugins"
		idx = 1
		res = (name, png, idx)
		self.list.append(res)
		
		mypixmap = mypath + "icons/nabskins.png"
		png = LoadPixmap(mypixmap)
		name = "Black Hole E2 Image Skins"
		idx = 2
		res = (name, png, idx)
		self.list.append(res)
		
		mypixmap = mypath + "icons/nabscript.png"
		png = LoadPixmap(mypixmap)
		name = "Black Hole Image Script"
		idx = 3
		res = (name, png, idx)
		self.list.append(res)
		
		mypixmap = mypath + "icons/nablangs.png"
		png = LoadPixmap(mypixmap)
		name = "Black Hole Image Boot Logo"
		idx = 4
		res = (name, png, idx)
		self.list.append(res)
		
		mypixmap = mypath + "icons/nabsettings.png"
		png = LoadPixmap(mypixmap)
		name = "Enigma2 Settings"
		idx = 5
		res = (name, png, idx)
		self.list.append(res)
		
		mypixmap = mypath + "icons/nabpicons.png"
		png = LoadPixmap(mypixmap)
		name = "Enigma2 Picons Packages"
		idx = 6
		res = (name, png, idx)
		self.list.append(res)
		
		mypixmap = mypath + "icons/nabuploads.png"
		png = LoadPixmap(mypixmap)
		name = "Latest 10 Uploads"
		idx = 7
		res = (name, png, idx)
		self.list.append(res)
		
		self["list"].list = self.list
	
		
		
	def KeyOk(self):
		self.sel = self["list"].getCurrent()
		if self.sel:
			self.sel = self.sel[2]
		
		self.url = "http://www.vuplus-community.net/bhaddons/index.php?op=outcat&cat=Cams"
		self.title = "Buuuuu"
		
		if self.sel == 1:
			self.url = "http://www.vuplus-community.net/bhaddons/index.php?op=outcat&cat=Plugins"
			self.title = "Black Hole Plugins"
		elif  self.sel == 2:
			self.url = "http://www.vuplus-community.net/bhaddons/index.php?op=outcat&cat=Skins"
			self.title = "Black Hole Skins"
		elif  self.sel == 3:
			self.url = "http://www.vuplus-community.net/bhaddons/index.php?op=outcat&cat=Scripts"
			self.title = "Black Hole Scripts"
		elif  self.sel == 4:
			self.url = "http://www.vuplus-community.net/bhaddons/index.php?op=outcat&cat=Logos"
			self.title = "Black Hole Boot Logo"
		elif  self.sel == 5:
			self.url = "http://www.vuplus-community.net/bhaddons/index.php?op=outcat&cat=Settings"
			self.title = "Black Hole Settings"
		elif  self.sel == 6:
			self.url = "http://www.vuplus-community.net/bhaddons/index.php?op=outcat&cat=Picons"
			self.title = "Black Hole Picons Packages"
		elif  self.sel == 7:
			self.url = "http://www.vuplus-community.net/bhaddons/index.php?op=outcat10_2"
			self.title = "Latest 10 Uploads"	
			
			
		downfile = "/tmp/cpanel.tmp"	
		if fileExists(downfile):
			os_remove(downfile)
		self.session.openWithCallback(self.connectionDone, Nab_ConnectPop, self.url, downfile)
			
			
	def connectionDone(self):
		downfile = "/tmp/cpanel.tmp"	
		if fileExists(downfile):
			self.session.open(Nab_downCat, self.title)
		else:
			nobox = self.session.open(MessageBox, "Sorry, Connection Failed.", MessageBox.TYPE_INFO)
		

class Nab_downCat(Screen):
	skin = """
	<screen position="80,95" size="560,405" title="Black Hole E2 Downloads Manager">
		<widget source="list" render="Listbox" position="10,16" size="540,345" scrollbarMode="showOnDemand" >
			<convert type="StringList" />
		</widget>
	</screen>"""
	
	def __init__(self, session, title):
		Screen.__init__(self, session)

		self.mytitle = title
		self.flist = []
		ivalue = ""
		step = 0
		if fileExists("/tmp/cpanel.tmp"):
			f = open("/tmp/cpanel.tmp",'r')
 			for line in f.readlines():
     				line = line.replace('\n', '')
				line = line.strip()
				if step == 0:
					ivalue = line
					step = 1
				else:
					res = (line, ivalue)
					self.flist.append(res)
					step = 0
		
 			f.close()
			os_remove("/tmp/cpanel.tmp")
		
		self["list"] = List(self.flist)
		self.onShown.append(self.setWindowTitle)

		self["actions"] = ActionMap(["WizardActions", "ColorActions"],
		{
			"ok": self.KeyOk,
			"back": self.close

		})

	def setWindowTitle(self):
		self.setTitle(self.mytitle)


	def KeyOk(self):
		self.sel = self["list"].getCurrent()
		if self.sel:
			self.myidf = self.sel[1]
			self.url = "http://www.vuplus-community.net/bhaddons/index.php?op=outfile&idf=" + self.myidf
				
			downfile = "/tmp/cpanel.tmp"	
			if fileExists(downfile):
				os_remove(downfile)
			self.session.openWithCallback(self.connectionDone, Nab_ConnectPop, self.url, downfile)
			
			
	def connectionDone(self):
		downfile = "/tmp/cpanel.tmp"	
		if fileExists(downfile):
			self.session.open(Nab_ShowDownFile, self.myidf, self.mytitle)
		else:
			nobox = self.session.open(MessageBox, "Sorry, Connection Failed.", MessageBox.TYPE_INFO)



class Nab_ShowPreviewFile(Screen):
	skin = """
	<screen position="0,0" size="1280,720" title="Black Hole E2 Preview" flags="wfNoBorder">
		<widget name="lab1" position="0,0" size="1280,720" zPosition="1" />
		<widget name="lab2" position="0,30" size="1280,30" zPosition="2" font="Regular;26" halign="center" valign="center" backgroundColor="red" foregroundColor="white" />
	</screen>"""
	
	def __init__(self, session, myprev):
		Screen.__init__(self, session)

		self["lab1"] = Pixmap()
		self["lab2"] = Label("Black Hole Preview: click ok to exit")
		self["actions"] = ActionMap(["WizardActions"],
		{
			"ok": self.close,
			"back": self.close,
		})

		self.fileP = myprev.replace('.tgz', '.jpg')
		self.onLayoutFinish.append(self.addonsconn)


	def addonsconn(self):
		myicon = "/tmp/" + self.fileP
		png = loadPic(myicon, 1280, 720, 0, 0, 0, 1)
		self["lab1"].instance.setPixmap(png)

	
class Nab_ShowDownFile(Screen):
	skin = """
	<screen position="80,95" size="560,405" title="Black Hole E2 Package Details">
		<widget name="infotext" position="10,15" size="540,315" font="Regular;20" />
		<ePixmap pixmap="skin_default/buttons/green.png" position="210,365" size="140,40" alphatest="on" />
		<widget name="key_green" position="210,365" zPosition="1" size="140,40" font="Regular;20" halign="center" valign="center" backgroundColor="#1f771f" transparent="1" />
		<ePixmap pixmap="skin_default/buttons/yellow.png" position="400,365" size="140,40" alphatest="on" />
		<widget name="key_yellow" position="400,365" zPosition="1" size="140,40" font="Regular;20" halign="center" valign="center" backgroundColor="#1f771f" transparent="1" />
	</screen>"""
	
	def __init__(self, session, myidf, category):
		Screen.__init__(self, session)

		self["key_green"] = Label("Download")
		self["key_yellow"] = Label("Preview")
		self["infotext"] = ScrollLabel()
		self.tcat = category
		
		step = 0
		strview = "TITLE: "
		if fileExists("/tmp/cpanel.tmp"):
			f = open("/tmp/cpanel.tmp",'r')
 			for line in f.readlines():
				line = nab_strip_html(line)
     				line = line.replace('\n', '')
				line = line.strip()
				if step == 0:
					self.fileN = line
					step = 1
				elif step == 1:
					strview += line
					strview += "\n\n"
					step = 2
				elif step == 2:
					strview += "By: "
					strview += line
					step = 3
				elif step == 3:
					strview += "                          " + line + "\n\n"
					step = 4
				elif step == 4:
					strview += "Size: " + line
					step = 5
				elif step == 5:
					strview += "                                Downloads: " + line + "\n"
					step = 6
				elif step == 6:
					strview += "---------------------------------------------------------------------\n" + line + "\n"
					step = 7
				else:
					strview += line + "\n"
		
 			f.close()
			os_remove("/tmp/cpanel.tmp")
		self["infotext"].setText(strview)

		self["actions"] = ActionMap(["WizardActions", "ColorActions", "DirectionActions"],
		{
			"ok": self.KeyGreend,
			"back": self.close,
			"green": self.KeyGreend,
			"yellow": self.KeyYellowd,
			"up": self["infotext"].pageUp,
			"down": self["infotext"].pageDown

		})
			
		
	def KeyYellowd(self):
		if (self.tcat != "Black Hole Skins" and self.tcat != "Black Hole Boot Logo"):
			nobox = self.session.open(MessageBox, "Sorry, the preview is available only for Skins and Bootlogo.", MessageBox.TYPE_INFO)
		else:
			self.fileP = self.fileN.replace('.tgz', '.jpg')
			self.url = '"http://www.vuplus-community.net/bhaddons/files/' + self.fileP + '"'
			cmd = "wget -O /tmp/" + self.fileP + " " + self.url
			self.session.openWithCallback(self.addonsconn2, Nab_ConnectPop, cmd, "N/A")
			
	def addonsconn2(self):
		self.session.open(Nab_ShowPreviewFile, self.fileP)
		
	def KeyGreend(self):
		self.url = '"http://www.vuplus-community.net/bhaddons/files/' + self.fileN + '"'
		cmd = "wget -O /tmp/" + self.fileN + " " + self.url
		self.session.openWithCallback(self.addonsconn, Nab_ConnectPop, cmd, "N/A")
		
	def addonsconn(self):
		message = "Do you want to install the Addon:\n " + self.fileN + " ?"
		ybox = self.session.openWithCallback(self.installadd, MessageBox, message, MessageBox.TYPE_YESNO)
		ybox.setTitle("Download Complete")
		
	def installadd(self, answer):
		if answer is True:
			mytype = 1
			if self.fileN.find('.ipk') != -1:
				mytype = 2
			
			if mytype == 1:
				dest = "/tmp/" + self.fileN
				mydir = getcwd()
				chdir("/")
				cmd = "tar -xzf " + dest
				rc = system(cmd)
				chdir(mydir)
				cmd = "rm -f " + dest
				rc = system(cmd)
				if fileExists("/usr/sbin/nab_e2_restart.sh"):
					rc = system("rm -f /usr/sbin/nab_e2_restart.sh")
					mybox = self.session.openWithCallback(self.hrestEn, MessageBox, "Enigma2 will be now hard restarted to complete package installation.\nPress ok to continue", MessageBox.TYPE_INFO)
					mybox.setTitle("Info")
				else:
					mybox = self.session.open(MessageBox, "Addon Succesfully Installed.", MessageBox.TYPE_INFO)
					mybox.setTitle("Info")
					self.close()
			
			elif mytype == 2:
				dest = "/tmp/" + self.fileN
				mydir = getcwd()
				chdir("/")
				cmd = "ipkg install " + dest
				cmd2 = "rm -f " + dest
				#rc = system(cmd)
				self.session.open(Console, title="Ipk Package Installation", cmdlist=[cmd, cmd2])
				chdir(mydir)
				#cmd = "rm -f " + dest
				#rc = system(cmd)
				

	def hrestEn(self, answer):
		rc = system("killall -9 enigma2")

class Nab_downPanel(Screen):
	skin = """
	<screen position="80,95" size="560,405" title="Black Hole E2 Manual Install BH Packages">
		<widget source="list" render="Listbox" position="10,16" size="540,380" scrollbarMode="showOnDemand" >
			<convert type="StringList" />
		</widget>
	</screen>"""
	
	def __init__(self, session):
		Screen.__init__(self, session)

		self.flist = []
		idx = 0
		pkgs = listdir("/tmp")
		for fil in pkgs:
			if fil.find('.tgz') != -1:
				res = (fil, idx)
				self.flist.append(res)
				idx = idx + 1
		
		self["list"] = List(self.flist)
		
		self["actions"] = ActionMap(["WizardActions", "ColorActions"],
		{
			"ok": self.KeyOk,
			"back": self.close

		})

	def KeyOk(self):
		self.sel = self["list"].getCurrent()
		if self.sel:
			self.sel = self.sel[0]
			message = "Do you want to install the Addon:\n " + self.sel + " ?"
			ybox = self.session.openWithCallback(self.installadd2, MessageBox, message, MessageBox.TYPE_YESNO)
			ybox.setTitle("Installation Confirm")

	def installadd2(self, answer):
		if answer is True:
			dest = "/tmp/" + self.sel
			mydir = getcwd()
			chdir("/")
			cmd = "tar -xzf " + dest
			rc = system(cmd)
			chdir(mydir)
			cmd = "rm -f " + dest
			rc = system(cmd)
			if fileExists("/usr/sbin/nab_e2_restart.sh"):
				rc = system("rm -f /usr/sbin/nab_e2_restart.sh")
				mybox = self.session.openWithCallback(self.hrestEn, MessageBox, "Enigma2 will be now hard restarted to complete package installation.\nPress ok to continue", MessageBox.TYPE_INFO)
				mybox.setTitle("Info")
			else:
				mybox = self.session.open(MessageBox, "Addon Succesfully Installed.", MessageBox.TYPE_INFO)
				mybox.setTitle("Info")
				self.close()

	def hrestEn(self, answer):
		rc = system("killall -9 enigma2")


class Nab_downPanelIPK(Screen):
	skin = """
	<screen position="80,95" size="560,405" title="Black Hole E2 Manual Install Ipk Packages">
		<widget source="list" render="Listbox" position="10,10" size="540,290" scrollbarMode="showOnDemand" >
			<convert type="StringList" />
		</widget>
		<widget name="warntext" position="0,305" size="560,100" font="Regular;20" halign="center" valign="center" backgroundColor="#1f771f" />
	</screen>"""
	
	def __init__(self, session):
		Screen.__init__(self, session)			

		self.flist = []
		idx = 0
		pkgs = listdir("/tmp")
		for fil in pkgs:
			if fil.find('.ipk') != -1:
				res = (fil, idx)
				self.flist.append(res)
				idx = idx + 1
		
		self["warntext"] = Label("Here you can install any kind of ipk packages.")
		self["list"] = List(self.flist)
		
		self["actions"] = ActionMap(["WizardActions", "ColorActions"],
		{
			"ok": self.KeyOk,
			"back": self.close

		})

	def KeyOk(self):
		self.sel = self["list"].getCurrent()
		if self.sel:
			self.sel = self.sel[0]
			message = "Do you want to install the Addon:\n " + self.sel + " ?"
			ybox = self.session.openWithCallback(self.installadd2, MessageBox, message, MessageBox.TYPE_YESNO)
			ybox.setTitle("Installation Confirm")

	def installadd2(self, answer):
		if answer is True:
			dest = "/tmp/" + self.sel
			mydir = getcwd()
			chdir("/")
			cmd = "ipkg install " + dest
			#rc = system(cmd)
			cmd2 = "rm -f " + dest
			self.session.open(Console, title="Ipk Package Installation", cmdlist=[cmd, cmd2])
			chdir(mydir)
			#cmd = "rm -f " + dest
			#rc = system(cmd)
			#mybox = self.session.open(MessageBox, "Addon Succesfully Installed.", MessageBox.TYPE_INFO)
			#mybox.setTitle("Info")
			#self.close()


class Nab_uninstPanel(Screen):
	skin = """
	<screen position="80,95" size="560,405" title="Black Hole E2 Uninstall Panel">
		<widget source="list" render="Listbox" position="10,16" size="540,380" scrollbarMode="showOnDemand" >
			<convert type="StringList" />
		</widget>
	</screen>"""
	
	def __init__(self, session):
		Screen.__init__(self, session)			

		self.flist = []
		idx = 0
		pkgs = listdir("/usr/uninstall")
		for fil in pkgs:
			if fil.find('.nab') != -1 or fil.find('.del') != -1:
				res = (fil, idx)
				self.flist.append(res)
				idx = idx + 1
		
		self["list"] = List(self.flist)
		
		self["actions"] = ActionMap(["WizardActions", "ColorActions"],
		{
			"ok": self.KeyOk,
			"back": self.close

		})
		
	def KeyOk(self):
		self.sel = self["list"].getCurrent()
		if self.sel:
			self.sel = self.sel[0]
			message = "Are you sure you want to Remove Package:\n " + self.sel + "?"
			ybox = self.session.openWithCallback(self.uninstPack, MessageBox, message, MessageBox.TYPE_YESNO)
			ybox.setTitle("Uninstall Confirmation")
		
	
	def uninstPack(self, answer):
		if answer is True:
			orig = "/usr/uninstall/" + self.sel
			cmd = "sh " + orig
			rc = system(cmd)
			mybox = self.session.open(MessageBox, "Addon Succesfully Removed.", MessageBox.TYPE_INFO)
			mybox.setTitle("Info")
			self.close()
			
		
class Nab_Stats(Screen):
	skin = """
	<screen position="80,95" size="560,405" title="Black Hole E2 Statistics">
		<widget name="infotext" position="10,15" size="540,315" font="Regular;20" />
	</screen>"""
	
	def __init__(self, session):
		Screen.__init__(self, session)	

		self["infotext"] = ScrollLabel()
		
		self["actions"] = ActionMap(["WizardActions"],
		{
			"ok": self.close,
			"back": self.close

		})		
		self.statshow()
		
		
	def statshow(self):
		if fileExists("/tmp/cpanel.tmp"):
			strview = "Black Hole Image Statistics:\n\n_____________________________________\n"
			step = 0
			f = open("/tmp/cpanel.tmp",'r')
		
 			for line in f.readlines():
				if step == 0:
					strview += "Total Connections:   \t"
				elif step == 1:
					strview += "Today Connections:   \t"
				elif step == 2:
					strview += "Available Forums:   \t"
				elif step == 3:
					step = step + 1
					continue
				elif step == 4:
					strview += "Shouts sent by users:\t"
				elif step == 5:
					step = step + 1
					continue
				elif step == 6:
					step = step + 1
					continue
				elif step == 7:
					strview += "Top downloaded File:\t"
				elif step == 8:
					strview += "Total Downloads:     \t"
					
				strview += line
				step = step + 1
			f.close()
			os_remove("/tmp/cpanel.tmp")
			self["infotext"].setText(strview)
				
class Nab_ConnectPop(Screen):
	skin = """
	<screen position="390,100" size="484,220" title="Black Hole E2" flags="wfNoBorder">
		<widget name="connect" position="0,0" size="484,250" zPosition="-1" pixmaps="skin_default/connection_1.png,skin_default/connection_2.png,skin_default/connection_3.png,skin_default/connection_4.png,skin_default/connection_5.png" transparent="1" />
		<widget name="lab1" position="10,180" halign="center" size="460,60" zPosition="1" font="Regular;20" valign="top" transparent="1" />
	</screen>"""
	
	def __init__(self, session, myurl, downfile):
		Screen.__init__(self, session)
		
		self["connect"] = MultiPixmap()
		self["connect"].setPixmapNum(0)
		self["lab1"] = Label("Wait please connection in progress ...")
		self.myurl = myurl
		self.downfile = downfile
		self.activityTimer = eTimer()
		if self.downfile == "N/A":
			self.activityTimer.timeout.get().append(self.updatepixWget)
		else:
			self.activityTimer.timeout.get().append(self.updatepix)
		
		self.onShow.append(self.startShow)
		self.onClose.append(self.delTimer)
		
	def startShow(self):
		self.curpix = 0
		self.count = 0
		self.activityTimer.start(300)
		
	def updatepixWget(self):
		self.activityTimer.stop()
		if self.curpix > 3:
			self.curpix = 0	
		if self.count > 8:
			self.curpix = 4
			self["lab1"].setText("Wait please, download in progress...")
		self["connect"].setPixmapNum(self.curpix)
		if self.count == 10:
			rc = system(self.myurl)
		if self.count == 11:
			self.close()
		
		self.activityTimer.start(120)
		self.curpix += 1
		self.count += 1


	def updatepix(self):
		self.activityTimer.stop()
		if self.curpix > 3:
			self.curpix = 0
			
		if self.count > 8:
			self.curpix = 4
			req = Request(self.myurl)
			try:
    				response = urlopen(req)
			except HTTPError, e:
    				self.close()
			except URLError, e:
    				self.close()
			else:
				self["lab1"].setText("Connection Established")
				html = response.read()
				out = open(self.downfile, "w")
				out.write(html)
				out.close()

				
		self["connect"].setPixmapNum(self.curpix)
		if self.count == 10:
			self.close()
		
		self.activityTimer.start(120)
		self.curpix += 1
		self.count += 1
		
	def delTimer(self):
		del self.activityTimer

