from Screens.Screen import Screen

from Screens.MessageBox import MessageBox
from Components.config import config, getConfigListEntry, ConfigSelection, ConfigYesNo, ConfigInteger, ConfigText, ConfigIP, NoSave, ConfigSubsection, ConfigNothing, KEY_LEFT, KEY_RIGHT, KEY_OK
from Components.ConfigList import *
from Components.Label import Label
from Components.ScrollLabel import ScrollLabel
from Components.ActionMap import ActionMap
from Screens.Console import Console
from Tools.Directories import fileExists
import os

TMP_FSTAB = "/tmp/fstab"
FSTAB = "/etc/fstab"

class DeliteMountWiz(Screen):
	skin = """
	<screen position="110,100" size="500,400" title="Black Hole E2 Mountpoints Wizard">
		<widget name="lab1" position="10,0" size="480,228" font="Regular;20" valign="center" transparent="1"/>
		<ePixmap pixmap="skin_default/div-h.png" position="1,228" size="498,2" />
		<widget name="infotext" position="10,240" size="490,80" font="Regular;18" />
		<ePixmap pixmap="skin_default/div-h.png" position="1,322" size="498,2" />
		<ePixmap pixmap="skin_default/buttons/red.png" position="20,350" size="140,40" alphatest="on" />
		<ePixmap pixmap="skin_default/buttons/green.png" position="170,350" size="140,40" alphatest="on" />
		<ePixmap pixmap="skin_default/buttons/yellow.png" position="320,350" size="140,40" alphatest="on" />
		<widget name="key_red" position="20,350" zPosition="1" size="140,40" font="Regular;20" halign="center" valign="center" backgroundColor="#9f1313" transparent="1" />
		<widget name="key_green" position="170,350" zPosition="1" size="140,40" font="Regular;20" halign="center" valign="center" backgroundColor="#1f771f" transparent="1" />
		<widget name="key_yellow" position="320,350" zPosition="1" size="140,40" font="Regular;20" halign="center" valign="center" backgroundColor="#a08500" transparent="1" />	
	</screen>"""
	
	def __init__(self, session):
		Screen.__init__(self, session)
		
		self["lab1"] = Label("")
		self["infotext"] = ScrollLabel("None found.")
		self["key_red"] = Label("Wizard Nfs")
		self["key_green"] = Label("Wizard Cifs")
		self["key_yellow"] = Label("Mount Editor")
		
		strview = "Welcome!!\nThis wizard will help you to mount and share your Pc, stabs or Nas Hdd.\nChoose the Cifs mode to share your Pc(Windows) or Nas Hdd.\nChoose the Nfs mode to share your boxes or Linux systems Hdd.\nCurrently mounted points:"
		idx = config.osd.language.value
		if idx == "it_IT":
			strview = "Benvenuto!!\nQuesto Wizard ti aiutera' a montare e condividere gli Hard disk del tuo Pc e dei tuoi Decoder.\nScegli il protocollo Cifs per montare unita' di un Pc(Windows) o Nas.\nScegli il protocollo Nfs per montare gli Hard disk di altri Decoder o di sistemi Linux.\nUnita' di rete correntemente montate:"
		
		self["lab1"].setText(strview)
		
		self["actions"] = ActionMap(["WizardActions", "ColorActions", "DirectionActions"],
		{
			"back": self.close,
			"up": self["infotext"].pageUp,
			"left": self["infotext"].pageUp,
			"down": self["infotext"].pageDown,
			"right": self["infotext"].pageDown,
			"red": self.NfsWiz,
			"green": self.CifsWiz,
			"yellow": self.MountMang
		})
		
		os.system ( "cp " + FSTAB + " " + TMP_FSTAB)
		self.updatetext()
		
	def MountMang(self):
		self.session.open(DeliteMountMang)
		
	def NfsWiz(self):
		self.session.open(DeliteNfsWiz)
		
	def CifsWiz(self):
		self.session.open(DeliteCifsWiz)
	
	def updatetext(self):
		strview = ""
		#rc = os.system("df > /tmp/ninfo.tmp")
		if fileExists("/proc/mounts"):
			f = open("/proc/mounts",'r')
 			for line in f.readlines():
				parts = line.strip().split()
				if parts[0].find('.') != -1:
					#totsp = (len(parts) -1)
					strview += parts[0] + "\t" + parts[1] + "\t" + parts[2] + "\n"

			f.close()
			#os.remove("/tmp/ninfo.tmp")
		if strview:		
			self["infotext"].setText(strview)


class DeliteCifsWiz(Screen):
	skin = """
	<screen position="60,100" size="600,400" title="E2 Cifs Wizard">
		<widget name="lab1" position="10,0" size="580,340" font="Regular;18" valign="center" transparent="1"/>
		<ePixmap pixmap="skin_default/buttons/red.png" position="230,350" size="140,40" alphatest="on" />		
		<widget name="key_red" position="230,350" zPosition="1" size="140,40" font="Regular;20" halign="center" valign="center" backgroundColor="#9f1313" transparent="1" />
	
	</screen>"""
	
	def __init__(self, session):
		Screen.__init__(self, session)
		
		self["lab1"] = Label("")
		self["key_red"] = Label("Continue ->")
	
		strview ="We are going to mount the hdd of your Windows Pc (SourceBox). Please make sure that:\n"
		strview +="-1) Your Windows Pc Network is up and running.\n-2) Your Windows Pc is configured to share a Network directory\n-3) The directory that you want to mount is configured to be shared.\n\n"
		strview +="To mount the Network volume you need the following informations:\n-1) Your Pc Ip address.\n-2) Your Pc directory available to share (user and password if assigned for directory access or leave 'guest').\n-3) The local directory of this stab in wich to mount the Pc volume (usually /media/net)."
		
		idx = config.osd.language.value
		if idx == "it_IT":
			strview ="Hai scelto di montare l'hd di un Pc Windows o di un'altra unita' esterna compatibile. Assicurati che:\n"
			strview +="-1) Il tuo Pc abbia la rete configurata e funzionante.\n-2) Il tuo Pc Windows abbia una directory configurata per la condivisione in rete.\n\n"
			strview +="Per completare la procedura devi avere le seguenti informazioni:\n-1) L'Indirizzo IP del Pc Windows.\n-2) La directory del tuo Pc configurata per la condivisione e i relativi user e password se settati per l'accesso alla stessa (altrimenti lascia 'guest').\n-3) La directory locale di questo Decoder nella quale vuoi montare l'unita' di rete (di solito /media/net)."
		
		self["lab1"].setText(strview)
		
		self["actions"] = ActionMap(["WizardActions", "ColorActions"],
		{
			"back": self.close,
			"red": self.continew
		})
		
		
	def continew(self):
		self.session.openWithCallback(self.myStop, NabMountNewNfs, "cifs")
		
	def myStop(self):
		self.close()


class DeliteNfsWiz(Screen):
	skin = """
	<screen position="60,100" size="600,400" title="E2 Nfs Wizard">
		<widget name="lab1" position="10,0" size="580,340" font="Regular;18" valign="center" transparent="1"/>
		<ePixmap pixmap="skin_default/buttons/red.png" position="230,350" size="140,40" alphatest="on" />		
		<widget name="key_red" position="230,350" zPosition="1" size="140,40" font="Regular;20" halign="center" valign="center" backgroundColor="#9f1313" transparent="1" />
	
	</screen>"""
	
	def __init__(self, session):
		Screen.__init__(self, session)
		
		self["lab1"] = Label("")
		self["key_red"] = Label("Continue ->")
	
		strview ="We are going to mount the hdd of another Stab or another system (SourceBox). Please make sure that:\n"
		strview +="-1) The SourceBox Nfs server is up and running. (As for example another Box with Bh Image).\n-2) The SourceBox Nfs server is configured to accept connections from the ip of this Box.\n-3) The SourceBox Nfs server is configured to share a directory.\n\n"
		strview +="To mount the SourceBox volume you need the following informations:\n-1) The SourceBox Ip address.\n-2) The SourceBox directory available to share.\n-3) The local directory of this Box in wich to mount the SourceBox volume (usually /media/net)."
		
		idx = config.osd.language.value
		if idx == "it_IT":
			strview ="Hai scelto di montare l'hd di un altro box o di un altro sistema Linux che chiameremo SourceBox. Assicurati che:\n"
			strview +="-1) Il SourceBox abbia un server Nfs installato. (Ad esempio un box provvisto di Bh Image).\n-2) Il server Nfs del SourceBox sia configurato per accettare connessioni dall'ip di questo box e abbia una directory accessibile.\n\n"
			strview +="Per completare la procedura devi avere le seguenti informazioni:\n-1) L'Indirizzo IP del SourceBox.\n-2) La directory del SourceBox configurata per la condivisione.\n-3) La directory locale di questo box nella quale vuoi montare l'unita' di rete (di solito /media/net)."
		
		self["lab1"].setText(strview)
		
		self["actions"] = ActionMap(["WizardActions", "ColorActions"],
		{
			"back": self.close,
			"red": self.continew
		})
		
		
	def continew(self):
		self.session.openWithCallback(self.myStop, NabMountNewNfs, "nfs")
		
	def myStop(self):
		self.close()

class NabMountNewNfs(Screen, ConfigListScreen):
	skin = """
	<screen position="140,120" size="440,300" title="E2 Mount Point Wizard">
		<widget name="config" position="10,10" size="420,240" scrollbarMode="showOnDemand" />
		<ePixmap pixmap="skin_default/buttons/red.png" position="40,250" size="140,40" alphatest="on" />
		<ePixmap pixmap="skin_default/buttons/green.png" position="220,250" size="140,40" alphatest="on" />
		<widget name="key_red" position="40,250" zPosition="1" size="140,40" font="Regular;20" halign="center" valign="center" backgroundColor="#9f1313" transparent="1" />
		<widget name="key_green" position="220,250" zPosition="1" size="140,40" font="Regular;20" halign="center" valign="center" backgroundColor="#1f771f" transparent="1" />
	</screen>"""
	def __init__(self, session, mytype):
		Screen.__init__(self, session)
		
		self.def_type = "nfs"
		self.def_share = "/export/hdd"
		if mytype == "cifs":
			self.def_type = "cifs"
			self.def_share = "/Share"
			
		self.def_server = [192,168,0,2]
		self.def_dir = "/media/net"
		self.def_nfs_options = "rw,nolock"
		self.def_cifs_options = ""
		self.def_username = "guest"
		self.def_password = "guest"
		
		if self.def_type == "nfs":
			self.type = ConfigSelection(default = self.def_type, choices = ["nfs"])
		else:
			self.type = ConfigSelection(default = self.def_type, choices = ["cifs"])
		self.server = ConfigIP(default = self.def_server)
		self.share = ConfigText(default = self.def_share, fixed_size = False)
		self.dir = ConfigText(default = self.def_dir, fixed_size = False)
		self.nfs_options = ConfigText(default = self.def_nfs_options, fixed_size = False)
		self.cifs_options = ConfigText(default = self.def_cifs_options, fixed_size = False)
		self.username = ConfigText(default = self.def_username, fixed_size = False) 
		self.password = ConfigText(default = self.def_password, fixed_size = False)
		
		self.list = []
		self.list.append(getConfigListEntry(_("Mount type"), self.type))
		self.list.append(getConfigListEntry(_("Server IP address"), self.server))
		self.list.append(getConfigListEntry(_("Server share directory"), self.share))
		self.list.append(getConfigListEntry(_("Local directory"), self.dir))
		if self.def_type == "nfs":
			self.list.append(getConfigListEntry(_("Mount options"), self.nfs_options))
		if self.type.value == "cifs":
			self.list.append(getConfigListEntry(_("Username"), self.username))
			self.list.append(getConfigListEntry(_("Password"), self.password))
		
		ConfigListScreen.__init__(self, self.list)
		
		self["key_red"] = Label(_("Save"))
		self["key_green"] = Label(_("Cancel"))
		
		
		self["actions"] = ActionMap(["WizardActions", "ColorActions"],
		{
			"red": self.savefst,
			"green": self.close,
			"back": self.close

		})
		
	def convertIP(self, ip):
		strIP = ip.split('.')
		ip = []
		for x in strIP:
			ip.append(int(x))
		return ip
		

	def savefst(self):
		changed = 0
		try:
			in_file = open( TMP_FSTAB, "r" )
		except IOError:
			self.close()
			return
		try:
			out_file = open( TMP_FSTAB + ".new", "w" )
		except IOError:
			self.close()
			return
		
		self.org_mp = self.dir.value
		
		if self.username.value == "":
			self.username.value = "guest"
		if self.password.value == "":
			self.password.value = "guest"

		if self.type.value == "nfs":
			f1 = "%d.%d.%d.%d" % tuple(self.server.value) + ":" + self.share.value
			f4 = self.nfs_options.value
		else:
			f1 = "//%d.%d.%d.%d" % tuple(self.server.value) + self.share.value
			f4 = "username=" + self.username.value + ",password=" + self.password.value
		
		while True:
			line = in_file.readline().strip()
			if line == "":
				break
			x = line.split()
			if x[1].strip() == self.org_mp and x[2] in ("nfs","cifs") :
				changed = 1
				
			out_file.write( line + "\n" )
		in_file.close()
		
		if not changed:
			out_file.write( "%-30s %-15s %-5s %-15s 1 0\n" % (f1, self.dir.value, self.type.value, f4) )
		out_file.close()
		
		if not changed:
			os.rename ( TMP_FSTAB + ".new", TMP_FSTAB )
			os.system ( "cp " + TMP_FSTAB + " " + FSTAB)	
			myarg = [f1, self.dir.value]
			self.session.openWithCallback(self.myStop, Nab_TestMount, myarg)
		else:
			message = "Mount Point " + self.dir.value + " exists."
			self.session.open(MessageBox, message, MessageBox.TYPE_ERROR)
	
	def myStop(self):
		self.close()


class Nab_TestMount(Screen):
	skin = """
	<screen position="140,120" size="440,300" title="E2 Mounter Test">
		<widget name="label1" position="10,10" size="420,230" font="Regular;20" halign="left" valign="left" />
		<ePixmap pixmap="skin_default/buttons/red.png" position="150,250" size="140,40" alphatest="on" />
		<widget name="key_red" position="150,250" zPosition="1" size="140,40" font="Regular;20" halign="center" valign="center" backgroundColor="#9f1313" transparent="1" />
	</screen>"""
	
	def __init__(self, session, title):
		Screen.__init__(self, session)
		
		self.mystate = 0
		self.mymount = title[0]
		strview = "Current Values:\n\nNetwork Path:\t" + title[0] + "\nLocal directory:\t" + title[1] + "\n\n"
		strview += "Click on continue to try to mount this network point."
		
		self["label1"] = Label(strview)
		self["key_red"] = Label(_("Continue ->"))
		
		self["actions"] = ActionMap(["WizardActions", "ColorActions"],
		{
			"red": self.mygo,
			"back": self.close,
			"ok": self.mountDone

		})	
		
	def mygo(self):
		if self.mystate == 0:
			title = self.mymount
			#self.session.open(Console, title = "Mounting...", cmdlist = ["net_mount.sh"], finishedCallback = self.close)
			mycmd1 = "mount " + title
			mycmd = "echo -e '------------------------------------\nTrying to mount your network point: " + title + "\n------------------------------------\n\n\n ' "
			self.session.open(Console, title="Mounting...", cmdlist=[mycmd, mycmd1])
			self.mystate = 1
			self["label1"].setText("Wizard Complete.\n\n\nClick on Continue to show the Mountpoints Panel.")
		else :
			self.mountDone()
			
	def mountDone(self):
		if self.mystate == 1:
			self.session.openWithCallback(self.myStop, DeliteMountMang)
		
	def myStop(self):
		self.close()

#--------------------------------------------------------------------------------------------------



class DeliteMountMang(Screen):
	skin = """
	<screen position="80,100" size="560,420" title="Black Hole E2 Mount manager">
		<widget name="lab1" position="10,0" size="540,30" font="Regular;20" valign="center" transparent="1"/>
		<ePixmap pixmap="skin_default/div-h.png" position="1,33" size="558,2" />
		<widget name="infotext" position="10,35" size="540,90" font="Regular;18" />
		<ePixmap pixmap="skin_default/div-h.png" position="1,123" size="558,2" />
		<widget name="lab2" position="10,125" size="540,30" font="Regular;20" valign="center" transparent="1"/>
		<ePixmap pixmap="skin_default/div-h.png" position="1,155" size="558,2" />
		<widget name="entries" position="10,160" size="540,200" scrollbarMode="showOnDemand" />
		<ePixmap name="redbutton" position="0,370" zPosition="1" size="140,40" pixmap="skin_default/buttons/red.png" transparent="1" alphatest="on" />
		<ePixmap name="greenbutton" position="140,370" zPosition="1" size="140,40" pixmap="skin_default/buttons/green.png" transparent="1" alphatest="on" />
		<ePixmap name="yellowbutton" position="280,370" zPosition="1" size="140,40" pixmap="skin_default/buttons/yellow.png" transparent="1" alphatest="on" />
		<ePixmap name="bluebutton" position="420,370" zPosition="1" size="140,40" pixmap="skin_default/buttons/blue.png" transparent="1" alphatest="on" />
		<widget name="red" position="0,370" zPosition="2" size="140,40" halign="center" valign="center" font="Regular;21" transparent="1" backgroundColor="red" shadowColor="black" shadowOffset="-1,-1" />
		<widget name="green" position="140,370" zPosition="2" size="140,40" halign="center" valign="center" font="Regular;21" transparent="1" backgroundColor="#1f771f" shadowColor="black" shadowOffset="-1,-1" />
		<widget name="yellow" position="280,370" zPosition="2" size="140,40" halign="center" valign="center" font="Regular;21" transparent="1" backgroundColor="#a08500" shadowColor="black" shadowOffset="-1,-1" />
		<widget name="blue" position="420,370" zPosition="2" size="140,40" halign="center" valign="center" font="Regular;21" transparent="1" backgroundColor="#18188b" shadowColor="black" shadowOffset="-1,-1" />
		
	</screen>"""
	
	def __init__(self, session):
		Screen.__init__(self, session)
		
		os.system ( "cp " + FSTAB + " " + TMP_FSTAB)
		
		self["lab1"] = Label(_("Currently mounted and connected:"))
		self["infotext"] = ScrollLabel("None found.")
		self["lab2"] = Label(_("All network points:"))
		self["red"] = Label(_("Mount"))
		self["green"] = Label(_("Umount"))
		self["yellow"] = Label(_("Delete"))
		self["blue"] = Label(_("Close"))
		
		self.list = []
		self["entries"] = ConfigList(self.list)
		
		self["actions"] = ActionMap(["OkCancelActions", "ColorActions", "CiSelectionActions"],
		{
			"left": self.keyLeft,
			"right": self.keyRight,
			"cancel": self.cancel,
			"red": self.mount,
			"green": self.umount,
			"yellow": self.remove,
			"blue": self.cancel,
		}, -2)
		
		self.createSetup()
		self.updatetext()
		
	def keyLeft(self):
#		self["entries"].handleKey(KEY_LEFT)
		pass	
	def keyRight(self):
#		self["entries"].handleKey(KEY_RIGHT)
		pass
	def updatetext(self):
		strview = ""
		#rc = os.system("df > /tmp/ninfo.tmp")
		if fileExists("/proc/mounts"):
			f = open("/proc/mounts",'r')
 			for line in f.readlines():
				parts = line.strip().split()
				if parts[0].find('.') != -1:
					#totsp = (len(parts) -1)
					strview += parts[0] + "\t" + parts[1] + "\t" + parts[2] + "\n"

			f.close()
		
		if strview == "":
			strview = "None found."
		self["infotext"].setText(strview)
		
	def createSetup(self):
		self.list = []
		try:
			file = open( TMP_FSTAB, "r" )
		except IOError:
			return
		while True:
			line = file.readline().strip()
			if line == "":
				break
			x = line.split()
			if x[2] == "nfs" or x[2] == "cifs":
				self.list.append(getConfigListEntry (x[1],ConfigNothing() ))
				
		file.close()
	
		self["entries"].l.setList(self.list)
			
	def mount(self):
		selection = self["entries"].getCurrent()
		if selection != None:
			selection = self["entries"].getCurrent()[0].strip()
			strview = ""
			f = open("/etc/fstab",'r')
 			for line in f.readlines():
				parts = line.strip().split()
				if parts[1] == selection:
					strview = parts[0].strip()

			f.close()
			if strview:
				mycmd1 = "mount " + strview
				mycmd = "echo -e '------------------------------------\nTrying to mount your network point: " + strview + "\n------------------------------------\n\n\n ' "
				self.session.open(Console, title="Mounting...", cmdlist=[mycmd, mycmd1], finishedCallback = self.updatetext)
	
	def umount(self):
		selection = self["entries"].getCurrent()
		if selection != None:
			selection = self["entries"].getCurrent()[0].strip()
			mycmd1 = "umount " + selection
			mycmd = "echo -e '------------------------------------\nUnmounting your network point: " + selection + "\n------------------------------------\n\n\n ' "
			self.session.open(Console, title="Unmounting...", cmdlist=[mycmd, mycmd1], finishedCallback = self.updatetext)
				
	
	def cancel(self):
		self.close()
	
	def remove(self):
		if self["entries"].getCurrent() == None:
			return
		
		mysel = self["entries"].getCurrent()[0].strip()
		os.system ("umount " + mysel)
		
		try:
			in_file = open( TMP_FSTAB, "r" )
		except IOError:
			self.close()
			return
		try:
			out_file = open( TMP_FSTAB + ".new", "w" )
		except IOError:
			self.close()
			return
		
		while True:
			line = in_file.readline().strip()
			if line == "":
				break
			x = line.split()
			if not x[2] in ("nfs","cifs") or not x[1] == self["entries"].getCurrent()[0]:
				out_file.write( line + "\n" )
		in_file.close()
		out_file.close()
		os.rename ( TMP_FSTAB + ".new", TMP_FSTAB )
		os.system ( "cp " + TMP_FSTAB + " " + FSTAB)
		
		self.createSetup()
		self.updatetext()
		self.session.open(MessageBox, "Mount Point deleted.", MessageBox.TYPE_INFO)

