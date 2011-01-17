from Screens.Screen import Screen

from Screens.MessageBox import MessageBox
from Components.ActionMap import ActionMap
from Components.ScrollLabel import ScrollLabel
from Components.Label import Label
from Tools.Directories import fileExists
from os import system, rename as os_rename, remove as os_remove


class DeliteOpenvpn(Screen):
	skin = """
	<screen position="80,150" size="560,310" title="Black Hole E2 OpenVpn Panel">
		<widget name="lab1" position="20,20" size="150,30" font="Regular;20" valign="center" transparent="1"/>
		<widget name="lab1a" position="170,16" size="370,60" font="Regular;20" valign="center" transparent="1"/>
		<widget name="lab2" position="20,90" size="150,30" font="Regular;20" valign="center" transparent="1"/>
		<widget name="labactive" position="170,90" size="250,30" font="Regular;20" valign="center" transparent="1"/>
		<widget name="lab3" position="20,160" size="150,30" font="Regular;20" valign="center" transparent="1"/>
		<widget name="labstop" position="170,160" size="100,30" font="Regular;20" valign="center"  halign="center" backgroundColor="red"/>
		<widget name="labrun" position="170,160" size="100,30" zPosition="1" font="Regular;20" valign="center"  halign="center" backgroundColor="green"/>
		<ePixmap pixmap="skin_default/buttons/red.png" position="0,260" size="140,40" alphatest="on" />
		<ePixmap pixmap="skin_default/buttons/green.png" position="140,260" size="140,40" alphatest="on" />
		<ePixmap pixmap="skin_default/buttons/yellow.png" position="280,260" size="140,40" alphatest="on" />
		<ePixmap pixmap="skin_default/buttons/blue.png" position="420,260" size="140,40" alphatest="on" />
		<widget name="key_red" position="0,260" zPosition="1" size="140,40" font="Regular;20" halign="center" valign="center" backgroundColor="#9f1313" transparent="1" />
		<widget name="key_green" position="140,260" zPosition="1" size="140,40" font="Regular;20" halign="center" valign="center" backgroundColor="#1f771f" transparent="1" />
		<widget name="key_yellow" position="280,260" zPosition="1" size="140,40" font="Regular;20" halign="center" valign="center" backgroundColor="#a08500" transparent="1" />
		<widget name="key_blue" position="420,260" zPosition="1" size="140,40" font="Regular;20" halign="center" valign="center" backgroundColor="#18188b" transparent="1" />
	</screen>"""
	
	def __init__(self, session):
		Screen.__init__(self, session)
		
		self["lab1"] = Label(_("Vpn Version: "))
		self["lab1a"] = Label(_("OpenVPN Panel - by Black Hole Team."))
		self["lab2"] = Label(_("Startup Module:"))
		self["labactive"] = Label(_("Inactive"))
		self["lab3"] = Label(_("Current Status:"))
		self["labstop"] = Label(_("Stopped"))
		self["labrun"] = Label(_("Running"))
		self["key_red"] = Label("Start")
		self["key_green"] = Label("Stop")
		self["key_yellow"] = Label("Set Active")
		self["key_blue"] = Label("Show Log")
		self.my_vpn_active = False
		self.my_vpn_run = False
				
		self["actions"] = ActionMap(["WizardActions", "ColorActions"],
		{
			"ok": self.close,
			"back": self.close,
			"red": self.restartVpn,
			"green": self.stopVpnstop,
			"yellow": self.activateVpn,
			"blue": self.Vpnshowlog

		})
		
		self.onLayoutFinish.append(self.updateVpn)
		
	def activateVpn(self):
		
		myline = 'AUTOSTART="all"'
		mymess = "OpenVpn Enabled. Autostart activated."
		if self.my_vpn_active == True:
			myline = 'AUTOSTART="none"'
			mymess = "OpenVpn disabled."
			
		if fileExists("/usr/bin/openvpn_script.sh"):
			inme = open("/usr/bin/openvpn_script.sh",'r')
			out = open("/usr/bin/openvpn_script.tmp",'w')
			for line in inme.readlines():
				if line.find('AUTOSTART="') != -1:
					line = myline + '\n'
				out.write(line)
			out.close()
			inme.close()
			
		if fileExists("/usr/bin/openvpn_script.tmp"):
			os_rename("/usr/bin/openvpn_script.tmp", "/usr/bin/openvpn_script.sh")
			system("chmod 0755 /usr/bin/openvpn_script.sh")
		
		mybox = self.session.open(MessageBox, mymess, MessageBox.TYPE_INFO)
		mybox.setTitle("Info")
		
		self.updateVpn()
		
	def restartVpn(self):
		if self.my_vpn_active == False:
			mybox = self.session.open(MessageBox, "You have to Activate OpenVpn before to start", MessageBox.TYPE_INFO)
			mybox.setTitle("Info")
		elif self.my_vpn_active == True and self.my_vpn_run == False:
			rc = system("/usr/bin/openvpn_script.sh start")
			rc = system("ps")
			self.updateVpn()
		elif self.my_vpn_active == True and self.my_vpn_run == True:
			rc = system("/usr/bin/openvpn_script.sh restart")
			rc = system("ps")
			self.updateVpn()
			
	def stopVpnstop(self):
		if self.my_vpn_run == True:
			rc = system("/usr/bin/openvpn_script.sh stop")
			rc = system("ps")
			self.updateVpn()
			
	def Vpnshowlog(self):
		self.session.open(DeliteVpnLog)
		
	def updateVpn(self):
		
		rc = system("ps > /tmp/nvpn.tmp")
		self["labrun"].hide()
		self["labstop"].hide()
		self["labactive"].setText("Inactive")
		self["key_yellow"].setText("Set Active")
		self.my_vpn_active = False
		self.my_vpn_run = False
		
		
		if fileExists("/usr/bin/openvpn_script.sh"):
			f = open("/usr/bin/openvpn_script.sh",'r')
 			for line in f.readlines():
				if line.find('AUTOSTART="all"') != -1:
					self["labactive"].setText("Active/Autostart enabled")
					self["key_yellow"].setText("Deactivate")
					self.my_vpn_active = True
								
			f.close()
				
				
		if fileExists("/tmp/nvpn.tmp"):
			f = open("/tmp/nvpn.tmp",'r')
 			for line in f.readlines():
				if line.find('/usr/sbin/openvpn') != -1:
					self.my_vpn_run = True

			f.close()
			os_remove("/tmp/nvpn.tmp")
			
		if self.my_vpn_run == True:
			self["labstop"].hide()
			self["labrun"].show()
			self["key_red"].setText(_("Restart"))
		else:
			self["labstop"].show()
			self["labrun"].hide()
			self["key_red"].setText(_("Start"))
			
	
class DeliteVpnLog(Screen):
	skin = """
	<screen position="80,100" size="560,400" title="Black Hole OpenVpn Log">
		<widget name="infotext" position="10,10" size="540,380" font="Regular;18" />
	</screen>"""
	
	def __init__(self, session):
		Screen.__init__(self, session)
		
		self["infotext"] = ScrollLabel("")
		self["actions"] = ActionMap(["WizardActions", "ColorActions"],
		{
			"ok": self.close,
			"back": self.close,
			"up": self["infotext"].pageUp,
			"down": self["infotext"].pageDown

		})
		
		strview = ""
		rc = system("tail /etc/openvpn/openvpn.log > /etc/openvpn/tmp.log")
		#tail /etc/openvpn/openvpn.log
		if fileExists("/etc/openvpn/tmp.log"):
			f = open("/etc/openvpn/tmp.log",'r')
 			for line in f.readlines():
				strview += line
				
			f.close()
			os_remove("/etc/openvpn/tmp.log")
		self["infotext"].setText(strview)




class DeliteSamba(Screen):
	skin = """
	<screen position="150,150" size="420,310" title="Black Hole Samba Panel">
		<widget name="lab1" position="20,50" size="200,30" font="Regular;20" valign="center" transparent="1"/>
		<widget name="labactive" position="220,50" size="150,30" font="Regular;20" valign="center" transparent="1"/>
		<widget name="lab2" position="20,100" size="200,30" font="Regular;20" valign="center" transparent="1"/>
		<widget name="labstop" position="220,100" size="100,30" font="Regular;20" valign="center"  halign="center" backgroundColor="red"/>
		<widget name="labrun" position="220,100" size="100,30" zPosition="1" font="Regular;20" valign="center"  halign="center" backgroundColor="green"/>
		<ePixmap pixmap="skin_default/buttons/red.png" position="0,260" size="140,40" alphatest="on" />
		<ePixmap pixmap="skin_default/buttons/green.png" position="140,260" size="140,40" alphatest="on" />
		<ePixmap pixmap="skin_default/buttons/yellow.png" position="280,260" size="140,40" alphatest="on" />
		<widget name="key_red" position="0,260" zPosition="1" size="140,40" font="Regular;20" halign="center" valign="center" backgroundColor="#9f1313" transparent="1" />
		<widget name="key_green" position="140,260" zPosition="1" size="140,40" font="Regular;20" halign="center" valign="center" backgroundColor="#1f771f" transparent="1" />
		<widget name="key_yellow" position="280,260" zPosition="1" size="140,40" font="Regular;20" halign="center" valign="center" backgroundColor="#a08500" transparent="1" />
	</screen>"""
	
	def __init__(self, session):
		Screen.__init__(self, session)
		
		self["lab1"] = Label(_("Samba Autostart: "))
		self["labactive"] = Label(_("Disabled"))
		self["lab2"] = Label(_("Current Status:"))
		self["labstop"] = Label(_("Stopped"))
		self["labrun"] = Label(_("Running"))
		self["key_red"] = Label("Start")
		self["key_green"] = Label("Stop")
		self["key_yellow"] = Label("Autostart")
		self.my_samba_active = False
		self.my_samba_run = False
				
		self["actions"] = ActionMap(["WizardActions", "ColorActions"],
		{
			"ok": self.close,
			"back": self.close,
			"red": self.NSambaStart,
			"green": self.NSambaStop,
			"yellow": self.NSambaset
		})
		
		self.onLayoutFinish.append(self.updateSamb)


	def NSambaStart(self):
		if self.my_samba_run == False:
			rc = system("smbd -D")
			rc = system("nmbd -D")
			self.updateSamb()
		
	def NSambaStop(self):
		if self.my_samba_run == True:
			rc = system("killall -9 nmbd")
			rc = system("killall -9 smbd")
			self.updateSamb()
		
	def NSambaset(self):
		mymess = "Samba Autostart Enabled."
		
		if fileExists("/etc/network/if-up.d/01samba-start"):
			rc = system("rm -f /etc/network/if-up.d/01samba-start")
			rc = system("rm -f /etc/network/if-down.d/01samba-kill")
			mymess = "Samba Autostart Disabled."
		else:
			out = open("/etc/network/if-up.d/01samba-start", "w")
			strview = "#!/bin/sh\nsmbd -D\nnmbd -D\n"
			out.write(strview)
			out.close()
			system("chmod 0755 /etc/network/if-up.d/01samba-start")
			
			out = open("/etc/network/if-down.d/01samba-kill", "w")
			strview = "#!/bin/sh\nkillall -9 smbd\nkillall -9 nmbd\n"
			out.write(strview)
			out.close()
			system("chmod 0755 /etc/network/if-down.d/01samba-kill")
		
		mybox = self.session.open(MessageBox, mymess, MessageBox.TYPE_INFO)
		mybox.setTitle("Info")
		self.updateSamb()


	def updateSamb(self):
		rc = system("ps > /tmp/nvpn.tmp")
		self["labrun"].hide()
		self["labstop"].hide()
		self["labactive"].setText("Disabled")
		self.my_samba_active = False
		self.my_samba_run = False
		
		
		if fileExists("/etc/network/if-up.d/01samba-start"):
			self["labactive"].setText("Enabled")
			self.my_samba_active = True
				
				
		if fileExists("/tmp/nvpn.tmp"):
			f = open("/tmp/nvpn.tmp",'r')
 			for line in f.readlines():
				if line.find('smbd') != -1:
					self.my_samba_run = True

			f.close()
			os_remove("/tmp/nvpn.tmp")
			
		if self.my_samba_run == True:
			self["labstop"].hide()
			self["labrun"].show()
		else:
			self["labstop"].show()
			self["labrun"].hide()
			
class DeliteTelnet(Screen):
	skin = """
	<screen position="190,150" size="340,310" title="Black Hole Telnet Panel">
		<widget name="lab1" position="20,30" size="300,60" font="Regular;20" valign="center" transparent="1"/>
		<widget name="lab2" position="20,150" size="150,30" font="Regular;20" valign="center" transparent="1"/>
		<widget name="labstop" position="170,150" size="100,30" font="Regular;20" valign="center"  halign="center" backgroundColor="red"/>
		<widget name="labrun" position="170,150" size="100,30" zPosition="1" font="Regular;20" valign="center"  halign="center" backgroundColor="green"/>
		<ePixmap pixmap="skin_default/buttons/red.png" position="20,260" size="140,40" alphatest="on" />
		<ePixmap pixmap="skin_default/buttons/green.png" position="180,260" size="140,40" alphatest="on" />
		<widget name="key_red" position="20,260" zPosition="1" size="140,40" font="Regular;20" halign="center" valign="center" backgroundColor="#9f1313" transparent="1" />
		<widget name="key_green" position="180,260" zPosition="1" size="140,40" font="Regular;20" halign="center" valign="center" backgroundColor="#1f771f" transparent="1" />
	</screen>"""
	
	def __init__(self, session):
		Screen.__init__(self, session)
		
		self["lab1"] = Label(_("You can disable Telnet Server and use ssh to login to your box."))
		self["lab2"] = Label(_("Current Status:"))
		self["labstop"] = Label(_("Stopped"))
		self["labrun"] = Label(_("Running"))
		self["key_red"] = Label("Enable")
		self["key_green"] = Label("Disable")
		self.my_telnet_active = False
				
		self["actions"] = ActionMap(["WizardActions", "ColorActions"],
		{
			"ok": self.close,
			"back": self.close,
			"red": self.NTelnetStart,
			"green": self.NTelnetStop
		})
		
		self.onLayoutFinish.append(self.updateTeln)


	def NTelnetStart(self):
		if self.my_telnet_active == False:
			if fileExists("/etc/inetd.conf"):
				inme = open("/etc/inetd.conf",'r')
				out = open("/etc/inetd.tmp",'w')
				for line in inme.readlines():
					if line.find('telnetd') != -1:
						line = line.replace('#', '')
					out.write(line)
				out.close()
				inme.close()
			
			if fileExists("/etc/inetd.tmp"):
				system("mv -f  /etc/inetd.tmp /etc/inetd.conf")
				rc = system("killall -HUP inetd")
				rc = system("ps")
				mybox = self.session.open(MessageBox, "Telnet service Enabled.", MessageBox.TYPE_INFO)
				mybox.setTitle("Info")
				self.updateTeln()
			
		
	def NTelnetStop(self):
		if self.my_telnet_active == True:
			if fileExists("/etc/inetd.conf"):
				inme = open("/etc/inetd.conf",'r')
				out = open("/etc/inetd.tmp",'w')
				for line in inme.readlines():
					if line.find('telnetd') != -1:
						line = "#" + line	
					out.write(line)
				out.close()
				inme.close()
			
			if fileExists("/etc/inetd.tmp"):
				system("mv -f  /etc/inetd.tmp /etc/inetd.conf")
				rc = system("killall -HUP inetd")
				rc = system("ps")
				mybox = self.session.open(MessageBox, "Telnet service Disabled.", MessageBox.TYPE_INFO)
				mybox.setTitle("Info")
				self.updateTeln()
		

	def updateTeln(self):
		self["labrun"].hide()
		self["labstop"].hide()
		self.my_telnet_active = False
		
		if fileExists("/etc/inetd.conf"):
			f = open("/etc/inetd.conf",'r')
 			for line in f.readlines():
				parts = line.strip().split()
				if parts[0] == 'telnet':
					self.my_telnet_active = True
								
			f.close()
			
		if self.my_telnet_active == True:
			self["labstop"].hide()
			self["labrun"].show()
		else:
			self["labstop"].show()
			self["labrun"].hide()
			
class DeliteFtp(Screen):
	skin = """
	<screen position="190,150" size="340,310" title="Black Hole Ftp Panel">
		<widget name="lab1" position="20,30" size="300,60" font="Regular;20" valign="center" transparent="1"/>
		<widget name="lab2" position="20,150" size="150,30" font="Regular;20" valign="center" transparent="1"/>
		<widget name="labstop" position="170,150" size="100,30" font="Regular;20" valign="center"  halign="center" backgroundColor="red"/>
		<widget name="labrun" position="170,150" size="100,30" zPosition="1" font="Regular;20" valign="center"  halign="center" backgroundColor="green"/>
		<ePixmap pixmap="skin_default/buttons/red.png" position="20,260" size="140,40" alphatest="on" />
		<ePixmap pixmap="skin_default/buttons/green.png" position="180,260" size="140,40" alphatest="on" />
		<widget name="key_red" position="20,260" zPosition="1" size="140,40" font="Regular;20" halign="center" valign="center" backgroundColor="#9f1313" transparent="1" />
		<widget name="key_green" position="180,260" zPosition="1" size="140,40" font="Regular;20" halign="center" valign="center" backgroundColor="#1f771f" transparent="1" />
	</screen>"""
	
	def __init__(self, session):
		Screen.__init__(self, session)
		
		self["lab1"] = Label(_("Ftpd service type: Vsftpd server (Very Secure FTP Daemon)"))
		self["lab2"] = Label(_("Current Status:"))
		self["labstop"] = Label(_("Stopped"))
		self["labrun"] = Label(_("Running"))
		self["key_red"] = Label("Enable")
		self["key_green"] = Label("Disable")
		self.my_ftp_active = False
				
		self["actions"] = ActionMap(["WizardActions", "ColorActions"],
		{
			"ok": self.close,
			"back": self.close,
			"red": self.NFtpStart,
			"green": self.NFtpStop
		})
		
		self.onLayoutFinish.append(self.updateFtp)


	def NFtpStart(self):
		if self.my_ftp_active == False:
			if fileExists("/etc/inetd.conf"):
				inme = open("/etc/inetd.conf",'r')
				out = open("/etc/inetd.tmp",'w')
				for line in inme.readlines():
					if line.find('vsftpd') != -1:
						line = line.replace('#', '')
					out.write(line)
				out.close()
				inme.close()
			
			if fileExists("/etc/inetd.tmp"):
				system("mv -f  /etc/inetd.tmp /etc/inetd.conf")
				rc = system("killall -HUP inetd")
				rc = system("ps")
				mybox = self.session.open(MessageBox, "Ftp service Enabled.", MessageBox.TYPE_INFO)
				mybox.setTitle("Info")
				self.updateFtp()
			
		
	def NFtpStop(self):
		if self.my_ftp_active == True:
			if fileExists("/etc/inetd.conf"):
				inme = open("/etc/inetd.conf",'r')
				out = open("/etc/inetd.tmp",'w')
				for line in inme.readlines():
					if line.find('vsftpd') != -1:
						line = "#" + line	
					out.write(line)
				out.close()
				inme.close()
			
			if fileExists("/etc/inetd.tmp"):
				system("mv -f  /etc/inetd.tmp /etc/inetd.conf")
				rc = system("killall -HUP inetd")
				rc = system("ps")
				mybox = self.session.open(MessageBox, "Ftp service Disabled.", MessageBox.TYPE_INFO)
				mybox.setTitle("Info")
				self.updateFtp()
		

	def updateFtp(self):
		self["labrun"].hide()
		self["labstop"].hide()
		self.my_ftp_active = False
		
		if fileExists("/etc/inetd.conf"):
			f = open("/etc/inetd.conf",'r')
 			for line in f.readlines():
				parts = line.strip().split()
				if parts[0] == 'ftp':
					self.my_ftp_active = True
								
			f.close()
			
		if self.my_ftp_active == True:
			self["labstop"].hide()
			self["labrun"].show()
		else:
			self["labstop"].show()
			self["labrun"].hide()
			

class BhDjmount(Screen):
	skin = """
	<screen position="center,center" size="602,305" title="Black Hole UPnP Client Panel">
		<widget name="lab1" position="20,30" size="580,60" font="Regular;20" valign="center" transparent="1"/>
		<widget name="lab2" position="20,150" size="300,30" font="Regular;20" valign="center" transparent="1"/>
		<widget name="labstop" position="320,150" size="150,30" font="Regular;20" valign="center" halign="center" backgroundColor="red"/>
		<widget name="labrun" position="320,150" size="150,30" zPosition="1" font="Regular;20" valign="center" halign="center" backgroundColor="green"/>
		<ePixmap pixmap="skin_default/buttons/red.png" position="125,260" size="150,30" alphatest="on"/>
		<ePixmap pixmap="skin_default/buttons/green.png" position="325,260" size="150,30" alphatest="on"/>
		<widget name="key_red" position="125,262" zPosition="1" size="150,25" font="Regular;20" halign="center" backgroundColor="transpBlack" transparent="1"/>
		<widget name="key_green" position="325,262" zPosition="1" size="150,25" font="Regular;20" halign="center" backgroundColor="transpBlack" transparent="1"/>
	</screen>"""
	
	def __init__(self, session):
		Screen.__init__(self, session)
		
		self["lab1"] = Label(_("djmount: mount server in /media/upnp"))
		self["lab2"] = Label(_("Current Status:"))
		self["labstop"] = Label(_("Stopped"))
		self["labrun"] = Label(_("Running"))
		self["key_red"] = Label("Enable")
		self["key_green"] = Label("Disable")
		self.my_serv_active = False
				
		self["actions"] = ActionMap(["WizardActions", "ColorActions"],
		{
			"ok": self.close,
			"back": self.close,
			"red": self.ServStart,
			"green": self.ServStop
		})
		
		self.onLayoutFinish.append(self.updateServ)


	def ServStart(self):
		if self.my_serv_active == False:
			rc = system("ln -s ../init.d/djmount /etc/rc3.d/S20djmount")
			rc = system("/etc/init.d/djmount start")
				
			mybox = self.session.open(MessageBox, "UPnP Client Enabled.", MessageBox.TYPE_INFO)
			mybox.setTitle("Info")
			self.updateServ()
			
		
	def ServStop(self):
		if self.my_serv_active == True:
			rc = system("/etc/init.d/djmount stop")
			os_remove("/etc/rc3.d/S20djmount")
				
			mybox = self.session.open(MessageBox, "UPnP Client Disabled.", MessageBox.TYPE_INFO)
			mybox.setTitle("Info")
			self.updateServ()
		

	def updateServ(self):
		self["labrun"].hide()
		self["labstop"].hide()
		rc = system("ps > /tmp/nvpn.tmp")
		self.my_serv_active = False
		
		if fileExists("/tmp/nvpn.tmp"):
			f = open("/tmp/nvpn.tmp",'r')
 			for line in f.readlines():
				if line.find('djmount') != -1:
					self.my_serv_active = True
			f.close()
			os_remove("/tmp/nvpn.tmp")
		
			
		if self.my_serv_active == True:
			self["labstop"].hide()
			self["labrun"].show()
		else:
			self["labstop"].show()
			self["labrun"].hide()
			
class BhUshare(Screen):
	skin = """
	<screen position="center,center" size="602,305" title="Black Hole UPnP Server Panel">
		<widget name="lab1" position="20,30" size="580,60" font="Regular;20" valign="center" transparent="1"/>
		<widget name="lab2" position="20,150" size="300,30" font="Regular;20" valign="center" transparent="1"/>
		<widget name="labstop" position="320,150" size="150,30" font="Regular;20" valign="center" halign="center" backgroundColor="red"/>
		<widget name="labrun" position="320,150" size="150,30" zPosition="1" font="Regular;20" valign="center" halign="center" backgroundColor="green"/>
		<ePixmap pixmap="skin_default/buttons/red.png" position="125,260" size="150,30" alphatest="on"/>
		<ePixmap pixmap="skin_default/buttons/green.png" position="325,260" size="150,30" alphatest="on"/>
		<widget name="key_red" position="125,262" zPosition="1" size="150,25" font="Regular;20" halign="center" backgroundColor="transpBlack" transparent="1"/>
		<widget name="key_green" position="325,262" zPosition="1" size="150,25" font="Regular;20" halign="center" backgroundColor="transpBlack" transparent="1"/>
	</screen>"""
	
	def __init__(self, session):
		Screen.__init__(self, session)
		
		self["lab1"] = Label(_("Ushare: UPnP media server"))
		self["lab2"] = Label(_("Current Status:"))
		self["labstop"] = Label(_("Stopped"))
		self["labrun"] = Label(_("Running"))
		self["key_red"] = Label("Enable")
		self["key_green"] = Label("Disable")
		self.my_serv_active = False
				
		self["actions"] = ActionMap(["WizardActions", "ColorActions"],
		{
			"ok": self.close,
			"back": self.close,
			"red": self.ServStart,
			"green": self.ServStop
		})
		
		self.onLayoutFinish.append(self.updateServ)


	def ServStart(self):
		if self.my_serv_active == False:
			rc = system("ln -s ../init.d/ushare /etc/rc3.d/S20ushare")
			rc = system("/etc/init.d/ushare start")
				
			mybox = self.session.open(MessageBox, "UPnP Server Enabled.", MessageBox.TYPE_INFO)
			mybox.setTitle("Info")
			self.updateServ()
			
		
	def ServStop(self):
		if self.my_serv_active == True:
			rc = system("/etc/init.d/ushare stop")
			os_remove("/etc/rc3.d/S20ushare")
				
			mybox = self.session.open(MessageBox, "UPnP Server Disabled.", MessageBox.TYPE_INFO)
			mybox.setTitle("Info")
			self.updateServ()
		

	def updateServ(self):
		self["labrun"].hide()
		self["labstop"].hide()
		rc = system("ps > /tmp/nvpn.tmp")
		self.my_serv_active = False
		
		if fileExists("/tmp/nvpn.tmp"):
			f = open("/tmp/nvpn.tmp",'r')
 			for line in f.readlines():
				if line.find('ushare') != -1:
					self.my_serv_active = True
			f.close()
			os_remove("/tmp/nvpn.tmp")
		
			
		if self.my_serv_active == True:
			self["labstop"].hide()
			self["labrun"].show()
		else:
			self["labstop"].show()
			self["labrun"].hide()

			
