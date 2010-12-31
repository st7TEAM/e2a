from Screens.Screen import Screen

from Screens.MessageBox import MessageBox
from Components.ActionMap import ActionMap
from Components.Label import Label
from Components.ScrollLabel import ScrollLabel
from Components.Pixmap import Pixmap
from Components.ConfigList import ConfigListScreen
from Components.config import getConfigListEntry, config, ConfigYesNo, ConfigText, ConfigNumber, NoSave, ConfigIP, ConfigSelection
from Tools.Directories import fileExists
from os import system


class DeliteNfs(Screen):
	skin = """
	<screen position="120,70" size="480,410" title="Black Hole Nfs Server Manager">
		<widget name="linactive" position="10,10" zPosition="1" pixmap="skin_default/icons/ninactive.png" size="32,32"  alphatest="on" />
		<widget name="lactive" position="10,10" zPosition="2" pixmap="skin_default/icons/nactive.png" size="32,32"  alphatest="on" />
		<widget name="lab1" position="50,10" size="350,30" font="Regular;20" valign="center"  transparent="1"/>
		<widget name="lab2" position="10,50" size="230,30" font="Regular;20" valign="center" transparent="1"/>
		<widget name="labclient" position="320,50" size="140,30" font="Regular;20" valign="center" backgroundColor="#4D5375"/>
		<widget name="lab3" position="10,100" size="150,30" font="Regular;20" valign="center" transparent="1"/>
		<widget name="labnetmask" position="320,100" size="140,30" font="Regular;20" valign="center" backgroundColor="#4D5375"/>
		<widget name="lab4" position="10,150" size="150,30" font="Regular;20" valign="center" transparent="1"/>
		<widget name="labflags" position="220,150" size="240,30" font="Regular;20" valign="center" backgroundColor="#4D5375"/>
		<widget name="sinactive" position="10,200" zPosition="1" pixmap="skin_default/icons/ninactive.png" size="32,32"  alphatest="on" />
		<widget name="sactive" position="10,200" zPosition="2" pixmap="skin_default/icons/nactive.png" size="32,32"  alphatest="on" />
		<widget name="lab5" position="50,200" size="200,30" font="Regular;20" valign="center" transparent="1"/>
		<widget name="labport" position="320,200" size="140,30" font="Regular;20" valign="center" backgroundColor="#4D5375"/>
		<widget name="lab6" position="10,250" size="150,30" font="Regular;20" valign="center" transparent="1"/>
		<widget name="labmdir" position="220,250" size="240,30" font="Regular;20" valign="center" backgroundColor="#4D5375"/>
		<widget name="lab7" position="10,300" size="150,30" font="Regular;20" valign="center" transparent="1"/>
		<widget name="labstop" position="160,300" size="100,30" font="Regular;20" valign="center"  halign="center" backgroundColor="red"/>
		<widget name="labrun" position="160,300" size="100,30" zPosition="1" font="Regular;20" valign="center"  halign="center" backgroundColor="green"/>
		<ePixmap pixmap="skin_default/buttons/red.png" position="20,360" size="140,40" alphatest="on" />
		<ePixmap pixmap="skin_default/buttons/green.png" position="170,360" size="140,40" alphatest="on" />
		<ePixmap pixmap="skin_default/buttons/yellow.png" position="320,360" size="140,40" alphatest="on" />
		<widget name="key_red" position="20,360" zPosition="1" size="140,40" font="Regular;20" halign="center" valign="center" backgroundColor="#9f1313" transparent="1" />
		<widget name="key_green" position="170,360" zPosition="1" size="140,40" font="Regular;20" halign="center" valign="center" backgroundColor="#1f771f" transparent="1" />
		<widget name="key_yellow" position="320,360" zPosition="1" size="140,40" font="Regular;20" halign="center" valign="center" backgroundColor="#a08500" transparent="1" />	
	</screen>"""
	
	def __init__(self, session):
		Screen.__init__(self, session)
		
		self["lab1"] = Label(_("Enable/Disable Nfs at Startup"))
		self["lactive"] = Pixmap()
		self["linactive"] = Pixmap()
		self["lab2"] = Label(_("Client Ip:"))
		self["labclient"] = Label()
		self["lab3"] = Label(_("Netmask:"))
		self["labnetmask"] = Label()
		self["lab4"] = Label(_("Flags:"))
		self["labflags"] = Label()
		self["lab5"] = Label(_("User Port:"))
		self["labport"] = Label()
		self["sactive"] = Pixmap()
		self["sinactive"] = Pixmap()
		self["lab6"] = Label(_("Mount Directory:"))
		self["labmdir"] = Label()
		self["lab7"] = Label(_("Status:"))
		self["labstop"] = Label(_("Stopped"))
		self["labrun"] = Label(_("Running !"))
		self["key_red"] = Label(_("Start"))
		self["key_green"] = Label(_("Stop"))
		self["key_yellow"] = Label(_("Setup"))
		
		self["lactive"].hide()
		self["sactive"].hide()
		self["labrun"].hide()
		
		self["actions"] = ActionMap(["WizardActions", "ColorActions"],
		{
			"ok": self.KeyOk,
			"back": self.close,
			"red": self.restartNfs,
			"green": self.stopNfs,
			"yellow": self.setupNfs
		})

		self.onLayoutFinish.append(self.updateNfs)
		
	def restartNfs(self):
		if self.my_nabnfs_state == False:
			mybox = self.session.open(MessageBox, "You have to Enable Nfs before to start", MessageBox.TYPE_INFO)
			mybox.setTitle("Info")
		else:
			rc = system("/usr/bin/nfs_server_script.sh stop")
			rc = system("/usr/bin/nfs_server_script.sh start")
			rc = system("ps")
			self.updateNfs()
	
	def stopNfs(self):
		if self.my_nabnfs_running == False:
			mybox = self.session.open(MessageBox, "Nfs Server is not running.", MessageBox.TYPE_INFO)
			mybox.setTitle("Info")
		else:
			rc = system("/usr/bin/nfs_server_script.sh stop")
			rc = system("ps")
			self.updateNfs()
	

	def updateNfs(self):
		self["lactive"].hide()
		self["linactive"].hide()
		self["sactive"].hide()
		self["sinactive"].hide()
		self["labrun"].hide()
		self["labstop"].hide()
		
		self.my_nabnfs_state = False
		self.my_nabnfs_running = False
		
		if fileExists("/usr/bin/nfs_server_script.sh"):
			f = open("/usr/bin/nfs_server_script.sh",'r')
 			for line in f.readlines():
				line = line.strip()
				if line.find('NFSSERVER_ON=') != -1:
					line = line[13:]
					if line == "1":
						self["lactive"].show()
						self.my_nabnfs_state = True
					else:
						self["linactive"].show()
				elif line.find('NFS_CL_IP=') != -1:
					line = line[10:]
					self["labclient"].setText(line)
				elif line.find('NFSNETMASKE=') != -1:
					line = line[12:]
					self["labnetmask"].setText(line)
				elif line.find('DIRECTORY=') != -1:
					line = line[10:]
					self["labmdir"].setText(line)
				elif line.find('OPTIONS=') != -1:
					line = line[8:]
					self["labflags"].setText(line)
				elif line.find('MOUNTD_PORT_ON=') != -1:
					line = line[15:]
					if line == "1":
						self["sactive"].show()
					else:
						self["sinactive"].show()
				elif line.find('MOUNTD_PORT=') != -1:
					line = line[12:]
					self["labport"].setText(line)
					
 			f.close()

		rc = system("ps > /tmp/ninadyn.tmp")
		check = False
		if fileExists("/tmp/ninadyn.tmp"):
			f = open("/tmp/ninadyn.tmp",'r')
 			for line in f.readlines():
				if line.find('/usr/sbin/rpc.mountd') != -1:
					check = True

			f.close()
			system("rm -f /tmp/ninadyn.tmp")
			
		if check == True:
			self["labstop"].hide()
			self["labrun"].show()
			self["key_red"].setText(_("Restart Nfs"))
			self.my_nabnfs_running = True
		else:
			self["labstop"].show()
			self["labrun"].hide()
			self["key_red"].setText(_("Start"))
			self.my_nabnfs_running = False


	def KeyOk(self):
		pass


	def setupNfs(self):
		self.session.openWithCallback(self.updateNfs, DeliteNfsSetup)


class DeliteNfsSetup(Screen, ConfigListScreen):
	skin = """
	<screen position="140,120" size="440,300" title="Black Hole Nfs Server Setup">
		<widget name="config" position="10,10" size="420,240" scrollbarMode="showOnDemand" />
		<ePixmap pixmap="skin_default/buttons/red.png" position="150,250" size="140,40" alphatest="on" />
		<widget name="key_red" position="150,250" zPosition="1" size="140,40" font="Regular;20" halign="center" valign="center" backgroundColor="#9f1313" transparent="1" />
	</screen>"""
	
	def __init__(self, session):
		Screen.__init__(self, session)
		
		self.list = []
		ConfigListScreen.__init__(self, self.list)
		self["key_red"] = Label(_("Save"))
		
		
		self["actions"] = ActionMap(["WizardActions", "ColorActions"],
		{
			"red": self.saveNfs,
			"back": self.close

		})
			
		self.updateList()
	
	
	def updateList(self):
		
		fflist = []
		fflist.append("ro")
		fflist.append("rw")
		fflist.append("ro,sync")
		fflist.append("rw,sync")
		fflist.append("ro,async")
		fflist.append("rw,async")
		fflist.append("ro,no_root_squash")
		fflist.append("rw,no_root_squash")
		fflist.append("ro,no_root_squash,sync")
		fflist.append("rw,no_root_squash,sync")
		fflist.append("ro,no_root_squash,async")
		fflist.append("rw,no_root_squash,async")
	
		self.nfs_active = NoSave(ConfigYesNo(default="False"))
		self.nfs_client = NoSave(ConfigIP(default=[192,168,0,2]))
		self.nfs_mask = NoSave(ConfigIP(default=[255,0,0,0]))
		self.nfs_flags = NoSave(ConfigSelection(fflist, default ="rw,no_root_squash,async"))
		self.nfs_portactive = NoSave(ConfigYesNo(default="False"))
		self.nfs_port = NoSave(ConfigNumber(default=2049))
		self.nfs_dir = NoSave(ConfigText(fixed_size = False, default="/media/hdd"))
		
		if fileExists("/usr/bin/nfs_server_script.sh"):
			f = open("/usr/bin/nfs_server_script.sh",'r')
 			for line in f.readlines():
				line = line.strip()
				if line.find('NFSSERVER_ON=') != -1:
					line = line[13:]
					if line == "1":
						self.nfs_active.value = True
					else:
						self.nfs_active.value = False
					nfs_active1 = getConfigListEntry(_("Activate Nfs Server"), self.nfs_active)
					self.list.append(nfs_active1)
				elif line.find('NFS_CL_IP=') != -1:
					line = line[10:]
					self.nfs_client.value = self.convertIP(line)
					nfs_client1 = getConfigListEntry(_("CLient IP"), self.nfs_client)
					self.list.append(nfs_client1)
				elif line.find('NFSNETMASKE=') != -1:
					line = line[12:]
					self.nfs_mask.value = self.convertIP(line)
					nfs_mask1 = getConfigListEntry(_("Netmask"), self.nfs_mask)
					self.list.append(nfs_mask1)
				elif line.find('DIRECTORY=') != -1:
					line = line[10:]
					self.nfs_dir.value = line
					nfs_dir1 = getConfigListEntry(_("Mount Directory"), self.nfs_dir)
					self.list.append(nfs_dir1)
				elif line.find('OPTIONS=') != -1:
					line = line[8:]
					self.nfs_flags.value = line
					nfs_flags1 = getConfigListEntry(_("Options"), self.nfs_flags)
					self.list.append(nfs_flags1)
				elif line.find('MOUNTD_PORT_ON=') != -1:
					line = line[15:]
					if line == "1":
						self.nfs_portactive.value = True
					else:
						self.nfs_portactive.value = False
					nfs_portactive1 = getConfigListEntry(_("Enable/Disable User Port"), self.nfs_portactive)
					self.list.append(nfs_portactive1)
				elif line.find('MOUNTD_PORT=') != -1:
					line = line[12:]
					self.nfs_port.value = int(line)
					nfs_port1 = getConfigListEntry(_("Port"), self.nfs_port)
					self.list.append(nfs_port1)
					
 			f.close()
		
		
		self["config"].list = self.list
		self["config"].l.setList(self.list)
		
		
	def saveNfs(self):
		
		myclient = (" %d.%d.%d.%d" % tuple(self.nfs_client.value))
		mymask =  (" %d.%d.%d.%d" % tuple(self.nfs_mask.value))
		
		if fileExists("/usr/bin/nfs_server_script.sh"):
			inme = open("/usr/bin/nfs_server_script.sh",'r')
			out = open("/usr/bin/nfs_server_script.tmp",'w')
			for line in inme.readlines():
				line = line.replace('\n', '')
				if line.find('NFSSERVER_ON=') != -1:
					strview = "0"
					if self.nfs_active.value == True:
						strview = "1"
					line = "NFSSERVER_ON=" + strview
				
				elif line.find('NFS_CL_IP=') != -1:
					line = "NFS_CL_IP=" + myclient.strip()
				
				elif line.find('NFSNETMASKE=') != -1:
					line = "NFSNETMASKE=" + mymask.strip()
				
				elif line.find('DIRECTORY=') != -1:
					line = "DIRECTORY=" + self.nfs_dir.value.strip()
				
				elif line.find('OPTIONS=') != -1:
					line = "OPTIONS=" + self.nfs_flags.value.strip()
				
				elif line.find('MOUNTD_PORT_ON=') != -1:
					strview = "0"
					if self.nfs_portactive.value == True:
						strview = "1"
					line = "MOUNTD_PORT_ON=" + strview
				
				elif line.find('MOUNTD_PORT=') != -1:
					strview = str(self.nfs_port.value)
					line = "MOUNTD_PORT=" + strview.strip()
				
				out.write(line + "\n")
				
			out.close()
			inme.close()
		
		else :
			self.session.open(MessageBox, "Sorry Nfs Server Script is Missing", MessageBox.TYPE_INFO)
			self.close()
			
		if fileExists("/usr/bin/nfs_server_script.tmp"):
			system("mv -f  /usr/bin/nfs_server_script.tmp /usr/bin/nfs_server_script.sh")
			system("chmod 0755 /usr/bin/nfs_server_script.sh")
		
		self.myStop()

		
	def myStop(self):
		self.close()
		
		
	def convertIP(self, ip):
		strIP = ip.split('.')
		ip = []
		for x in strIP:
			ip.append(int(x))
		return ip
	