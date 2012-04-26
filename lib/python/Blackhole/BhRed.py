from Screens.Screen import Screen
from Screens.MessageBox import MessageBox
from Components.ActionMap import ActionMap
from Components.Label import Label
from Components.config import config, configfile
from Components.Console import Console
from Components.MenuList import MenuList
from Components.MultiContent import MultiContentEntryText, MultiContentEntryPixmapAlphaTest
from Tools.LoadPixmap import LoadPixmap
from Tools.Directories import fileExists, pathExists, createDir
from os import system, remove as os_remove
from BhUtils import DeliteGetSkinPath, BhU_check_proc_version
from enigma import eListboxPythonMultiContent, gFont, eTimer

# from Screens.Standby import TryQuitMainloop
#from Components.Sources.List import List
#from enigma import eDVBDB


class UniverseList(MenuList):
	def __init__(self, enableWrapAround = False):
		MenuList.__init__(self, [], enableWrapAround, eListboxPythonMultiContent)
		self.l.setFont(0, gFont("Regular", 24))
		self.l.setItemHeight(106)
		


class BhRedDisabled(Screen):
	skin = """
	<screen position="center,center" size="700,300" title="Expand your universe.">
		<widget name="lab1" position="20,20" size="660,260" font="Regular;20" />
	</screen>"""

	def __init__(self, session):
		Screen.__init__(self, session)
		
		msg = "Sorry no space available to expand your universe.\n\nTo enable parallel dimensions you you need a dedicated Usb stick.\n\nInstructions:\n1) Format your Usb stick \n   -click on blue -> blue -> Usb Format Wizard\n\n2) Map the new formatted stick to \"universe\"\n   -click on blue -> blue -> Devices Manager."
		self["lab1"] = Label(msg)
		self["actions"] = ActionMap(["WizardActions"],
		{
			"ok": self.close,
			"back": self.close
		}, -1)
		
class BhRedWrong(Screen):
	skin = """
	<screen position="center,center" size="700,330" title="Outdated universes.">
		<widget name="lab1" position="20,10" size="660,260" font="Regular;20" />
		<ePixmap pixmap="skin_default/buttons/red.png" position="146,280" size="140,40" alphatest="on" />
		<ePixmap pixmap="skin_default/buttons/green.png" position="432,280" size="140,40" alphatest="on" />
		<widget name="key_red" position="146,280" zPosition="1" size="140,40" font="Regular;20" halign="center" valign="center" backgroundColor="#9f1313" transparent="1" />
		<widget name="key_green" position="432,280" zPosition="1" size="140,40" font="Regular;20" halign="center" valign="center" backgroundColor="#1f771f" transparent="1"/>
	</screen>"""

	def __init__(self, session):
		Screen.__init__(self, session)
		
		self["key_red"] = Label("Big Bang")
		self["key_green"] = Label("Exit")
		msg = "Sorry your parallel universes are older than your Black Hole world.\nYou need to reinizialize the system reformatting your Usb stick or generating a Bing Bang.\n"
		self["lab1"] = Label(msg)
		self["actions"] = ActionMap(["WizardActions", "ColorActions"],
		{
			"red": self.gotobingBang,
			"green": self.close,
			"back": self.close
		})
		
	def gotobingBang(self):
		msg = "The Big Bang will collapse all the parallel universes into the original matrix Black Hole.\nThis means that all your parallel universes will be destroyed turning back into Black Hole timespace.\nWarning, all the data stored in your parallel universes will be lost.\nAre you sure to start the Bing Bang?"
		self.session.openWithCallback(self.startbigBang, MessageBox, msg, MessageBox.TYPE_YESNO)
		
	def startbigBang(self, answer):
		if answer == True:
			self.session.open(BhBigBang)
			self.close()

class BhRedPanel(Screen):
	skin = """
	<screen position="center,center" size="1000,530" title="Black Hole Parallel Universes Teleportation">
		
		<widget name="list" position="10,0" size="580,450" scrollbarMode="showOnDemand" transparent="1"   />
		
		<ePixmap pixmap="skin_default/div-v.png" position="590,0" size="2,450" alphatest="on" />
		<widget name="lab1" position="600,10" size="400,30" font="Regular;24" halign="center" foregroundColor="#9f1313" transparent="1"/>
		<widget name="lab2" position="600,60" size="400,390" font="Regular;20" valign="top" transparent="1"/>
		<ePixmap pixmap="skin_default/div-h.png" position="0,450" size="500,2" alphatest="on" />
		<ePixmap pixmap="skin_default/div-h.png" position="500,450" size="500,2" alphatest="on" />
    		<ePixmap pixmap="skin_default/buttons/red.png" position="145,470" size="140,40" alphatest="on" />
		<ePixmap pixmap="skin_default/buttons/green.png" position="430,470" size="140,40" alphatest="on" />
		<ePixmap pixmap="skin_default/buttons/yellow.png" position="715,470" size="140,40" alphatest="on" />
		<widget name="key_red" position="145,470" zPosition="1" size="140,40" font="Regular;20" halign="center" valign="center" backgroundColor="#9f1313" transparent="1" />
		<widget name="key_green" position="430,470" zPosition="1" size="140,40" font="Regular;20" halign="center" valign="center" backgroundColor="#1f771f" transparent="1"/>
		<widget name="key_yellow" position="715,470" zPosition="1" size="140,40" font="Regular;20" halign="center" valign="center" backgroundColor="#a08500" transparent="1" />
    	</screen>"""
	
	def __init__(self, session):
		Screen.__init__(self, session)
		
		self["key_red"] = Label("Jump to...")
		self["key_green"] = Label("Big Bang")
		self["key_yellow"] = Label("Exit")
		self["lab1"] = Label()
		self["lab2"] = Label()
		self.current_universe = self.destination = ""
		self.jump_on_close = False
		
		self.list = []
		self["list"] = UniverseList()
		
		self["actions"] = ActionMap(["WizardActions", "ColorActions"],
		{
			"back": self.close,
			"ok": self.checkdesT,
			"red": self.checkdesT,
			"green": self.check_origin,
			"yellow": self.close
		}, -1)
		
		
		self.onClose.append(self.closE)
		self.onShow.append(self.updateList)
		
	def updateList(self):
		mypath = DeliteGetSkinPath()
		rc = system("df -h > /tmp/syinfo.tmp")
		
		mypixmap = mypath + "icons/icon_home_BH.png"
		png = LoadPixmap(mypixmap)
		name = "Black Hole"
		title = MultiContentEntryText(pos = (120, 30), size = (480, 50), font=0, text=name)
               	png = MultiContentEntryPixmapAlphaTest(pos = (0, 3), size = (100, 100), png = png)		
		self.list.append([name, title, png])
		
		mypixmap = mypath + "icons/icon_avalon.png"
		png = LoadPixmap(mypixmap)
		name = "Avalon"
		title = MultiContentEntryText(pos = (120, 30), size = (480, 50), font=0, text=name)
               	png = MultiContentEntryPixmapAlphaTest(pos = (0, 3), size = (100, 100), png = png)		
		self.list.append([name, title, png])


		mypixmap = mypath + "icons/icon_chaos.png"
		png = LoadPixmap(mypixmap)
		name = "Chaos"
		title = MultiContentEntryText(pos = (120, 30), size = (480, 50), font=0, text=name)
               	png = MultiContentEntryPixmapAlphaTest(pos = (0, 3), size = (100, 100), png = png)		
		self.list.append([name, title, png])
		
		mypixmap = mypath + "icons/icon_ghost.png"
		png = LoadPixmap(mypixmap)
		name = "Ghost"
		title = MultiContentEntryText(pos = (120, 30), size = (480, 50), font=0, text=name)
               	png = MultiContentEntryPixmapAlphaTest(pos = (0, 3), size = (100, 100), png = png)		
		self.list.append([name, title, png])
		
		self["list"].setList(self.list)
		
		self.current_universe = self.whereIAm()
		
		txt = "You are in %s universe." % (self.current_universe)
		self["lab1"].setText(txt)
		
		btot = buse = bempty = utot = uuse = uempty = ""
		f = open("/tmp/syinfo.tmp",'r')
		for line in f.readlines():
			parts = line.split()
			tot = len(parts) -1
			if parts[tot].strip() == "/":
				btot = parts[(tot - 4)].strip()
				buse = parts[(tot - 1)].strip()
				bempty = parts[(tot - 2)].strip()
			elif parts[tot].strip() == "/universe":
				utot = parts[(tot - 4)].strip()
				uuse = parts[(tot - 1)].strip()
				uempty = parts[(tot - 2)].strip()
				break
		f.close()
		os_remove("/tmp/syinfo.tmp")
		
		text = "Black Hole details:\nBlack Hole is the original matrix of all parallel universes and resides in its phisycal space.\n"
		text += "Estimated size: %s \n" % (btot)
		text += "Occupied space: %s \n" % (buse)
		text += "Empty space: %s \n\n" % (bempty)

		text += "Parallel Universes details:\nParallel universes share the same space because are all togheter in the same place but in different dimensions.\n"
		text += "Estimated size: %s \n" % (utot)
		text += "Occupied space: %s \n" % (uuse)
		text += "Empty space: %s \n\n" % (uempty)

		self["lab2"].setText(text)
		
		pos = 0
		sel = self["list"].getCurrent()
		for x in self.list:
			if x[0] == self.current_universe:
				self["list"].moveToIndex(pos)
				break
			pos += 1
		

	def whereIAm(self):
		ret = "Black Hole"
		all = ["Avalon", "Chaos", "Ghost"]
		f = open("/proc/mounts",'r')
		for line in f.readlines():
			if line.find('/usr ') != -1:
				for a in all:
					if line.find(a) != -1:
						ret = a
				break
		f.close()
		return ret
		
	def checkdesT(self):
		sel = self["list"].getCurrent()
		self.destination = sel[0]
		
		if self.current_universe == self.destination:
			msg = "You are already in %s universe." % (self.destination)
			self.session.open(MessageBox, msg, MessageBox.TYPE_INFO)
		else :
			self.askjumpConfirm()

	def askjumpConfirm(self):
		msg = "We are going to jump into %s universe.\nPlease remember that all you will do in this universe like to install sofware, skins or plugins will have no effects on the other universes.\nAre you sure to jump?" % (self.destination)
		self.session.openWithCallback(self.prEjumP, MessageBox, msg, MessageBox.TYPE_YESNO)
		
	
	def prEjumP(self, answer):
		if answer == True:
			rc = system("/usr/bin/StartBhCam stop")
			mvi = "/usr/share/" + self.destination + ".mvi"
			mvi = mvi.replace(' ', '_')
			cmd = "cp %s /bin/jump_screen.mvi" % (mvi)
			rc = system(cmd)
			self.jumP()
		else:
			pass
			
	def jumP(self):
# build dirs		
		path = "/universe/" + self.destination
		path1 = path + "/etc"
		path2 = path + "/usr"
		if self.destination != "Black Hole":
			if not pathExists(path):
				createDir(path)
			if not pathExists(path1):
				createDir(path1)
			if not pathExists(path2):
				createDir(path2)
# build bootup file
		if self.destination == "Black Hole":
			if fileExists("/bin/bh_parallel_mount"):
				os_remove("/bin/bh_parallel_mount")
		else:
			out = open("/bin/bh_parallel_mount",'w')
			line = "#!/bin/sh\n\n\nmount -t unionfs -o dirs=%s:/etc=ro none /etc\n" % (path1)
			out.write(line)
			line = "mount -t unionfs -o dirs=%s:/usr=ro none /usr\n\nexit 0\n" % (path2)
			out.write(line)
			out.close()
			system("chmod 0755 /bin/bh_parallel_mount")
# build jump file				
		out = open("/bin/bh_jump",'w')
		line = "#!/bin/sh\n\ninit 4\numount -l /etc\numount -l /usr\n"
		out.write(line)
		if self.destination != "Black Hole":
			line = "sleep 1\n\nmount -t unionfs -o dirs=%s:/etc=ro none /etc\n" % (path1)
			out.write(line)
			line = "mount -t unionfs -o dirs=%s:/usr=ro none /usr\n" % (path2)
			out.write(line)
		line = "\ninit 3\nexit 0\n"
		out.write(line)
		out.close()
		rc = system("chmod 0755 /bin/bh_jump")
# jump.. bye bye
		configfile.save()
		self.jump_on_close = True
		self.close()
		
			
	def check_origin(self):
		origin = self.whereIAm()
		if origin != "Black Hole":
			msg = "The Big Bang will collapse all the parallel universes into the original matrix Black Hole.\nThis means that all your parallel universes will be destroyed turning back into Black Hole timespace.\nFor this reason you have to safe yourself jumping into Black Hole universe before to start the big bang."
			self.session.open(MessageBox, msg, MessageBox.TYPE_INFO)
		else :
			msg = "The Big Bang will collapse all the parallel universes into the original matrix Black Hole.\nThis means that all your parallel universes will be destroyed turning back into Black Hole timespace.\nWarning, all the data stored in your parallel universes will be lost.\nAre you sure to start the Bing Bang?"
			self.session.openWithCallback(self.startbigBang, MessageBox, msg, MessageBox.TYPE_YESNO)
			
	def startbigBang(self, answer):
		if answer == True:
			self.session.openWithCallback(self.updateList, BhBigBang)
		
			
	def closE(self):
		if self.jump_on_close == True:
			Console().ePopen("/bin/bh_jump")
			
			
			
class BhBigBang(Screen):
	skin = """
	<screen position="center,center" size="1270,720" title="Big Bang" backgroundColor="#000000"  flags="wfNoBorder" >
		<widget name="lab1" position="320,230" size="590,30" backgroundColor="#000000" halign="center"  valign="center" font="Regular;30" />
		<widget name="lab2" position="585,260" size="70,200" backgroundColor="#000000" halign="center" valign="center" font="Regular;50" />
	</screen>"""

	def __init__(self, session):
		Screen.__init__(self, session)
		
		self["lab1"] = Label("Wait please Big Bang in progress")
		self["lab2"] = Label()
		self["actions"] = ActionMap(["WizardActions"],
		{
			"back": self.close
		})
	
		self.labtext = "Wait please Big Bang in progress"
		self.activityTimer = eTimer()
		self.activityTimer.timeout.get().append(self.updatepiX)
		self.onShow.append(self.startShow)
		self.onClose.append(self.delTimer)
		
	def startShow(self):
		self.count = 0
		self.activityTimer.start(10)
		
	def updatepiX(self):
		self.activityTimer.stop()
		if self.count == 0:
			self["lab2"].setText("3")
			cmd = "rm -f -r /universe/Avalon"
			rc = system(cmd)
		elif self.count == 1:
			self["lab2"].setText("2")
			cmd = "rm -f -r /universe/Chaos"
			rc = system(cmd)
		elif self.count == 2:
			self["lab2"].setText("1")
			cmd = "rm -f -r /universe/Ghost"
			rc = system(cmd)
		elif self.count == 3:
			self["lab2"].setText("0")
			rc = system("chmod a+w /universe/.buildv")
			rc = system(" rm -f /universe/.buildv")
		else:
			self.session.openWithCallback(self.bigEnd, MessageBox, "Your Universes have been reinizialized. You can start now to rebuils your worlds.", MessageBox.TYPE_INFO)
		
			
		self.activityTimer.start(1500)
		self.count += 1
		
		
	def bigEnd(self, answer):
		self.close()
		
	def delTimer(self):
		del self.activityTimer



class BhRedp:
	def __init__(self):
		self["BhRedp"] = ActionMap( [ "InfobarExtensions" ],
			{
				"BhRedpshow": (self.showBhRedp),
			})
			
		
			
			
			

	def showBhRedp(self):
		
		mounted = False
		bh_ver = BhU_check_proc_version()
		un_ver = bh_ver
		if fileExists("/universe/.buildv"):
			f = open("/universe/.buildv",'r')
			un_ver = f.readline().strip()
			f.close()
		else:
			out = open("/universe/.buildv",'w')
			out.write(bh_ver)
			out.close()
			system("chmod a-w /universe/.buildv")
		
		f = open("/proc/mounts",'r')
		for line in f.readlines():
			if line.find('/universe') != -1:
				if line.find('ext') != -1:
					mounted = True
					break
		f.close()
		if mounted == False:
			self.session.openWithCallback(self.callBhAction, BhRedDisabled)
		else:
			if un_ver == bh_ver:
				self.session.openWithCallback(self.callBhAction, BhRedPanel)
			else:
				self.session.openWithCallback(self.callBhAction, BhRedWrong)
		
		

	def callBhAction(self, *args):
		if len(args):
			(actionmap, context, action) = args
			actionmap.action(context, action)
			
