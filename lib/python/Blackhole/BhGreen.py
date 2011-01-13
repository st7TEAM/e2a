from Screens.Screen import Screen
from Components.ActionMap import ActionMap
from Components.PluginComponent import plugins
from Components.Sources.List import List
from Components.Label import Label
from Components.config import config, configfile
from Screens.MessageBox import MessageBox
from Plugins.Plugin import PluginDescriptor
from Tools.Directories import resolveFilename, SCOPE_SKIN_IMAGE
from Tools.LoadPixmap import LoadPixmap
from BhAddons import DeliteAddons
from BhScript import DeliteScript


class DeliteGreenPanel(Screen):
	def __init__(self, session):
		Screen.__init__(self, session)
		
		self.list = []
		self["list"] = List(self.list)
		self.updateList()
		
		self["actions"] = ActionMap(["WizardActions", "ColorActions"],
		{
			"ok": self.save,
			"back": self.close,
			"red": self.Redc,
			"green": self.Fastplug,
			"yellow": self.Addons,
			"blue": self.NabScript
		}, -1)
		

	def save(self):
		self.run()
	
	def run(self):
		mysel = self["list"].getCurrent()
		if mysel:
			plugin = mysel[3]
			plugin(session=self.session)
		
	def updateList(self):
		self.list = [ ]
		self.pluginlist = plugins.getPlugins(PluginDescriptor.WHERE_PLUGINMENU)
		for plugin in self.pluginlist:
			#self.list.append(PluginEntryComponent(plugin))
			if plugin.icon is None:
				png = LoadPixmap(resolveFilename(SCOPE_SKIN_IMAGE, "skin_default/icons/plugin.png"))
			else:
				png = plugin.icon
			res = (plugin.name, plugin.description, png, plugin)
			self.list.append(res)
		
		self["list"].list = self.list

	def Addons(self):
		self.session.open(DeliteAddons)
		
	def Redc(self):
		self.session.open(DeliteSetupFp)
		
	def NabScript(self):
		self.session.open(DeliteScript)
		
	def Fastplug(self):
		result = ""
		check = False
		myplug = config.delite.fp.value
		for plugin in self.list:
			result = plugin[3].name
			if result == myplug:
				runplug = plugin[3]
				check = True
				break
		
		if check == True:
			runplug(session=self.session)
		else:
			mybox = self.session.open(MessageBox, "Fast Plugin not found. You have to setup Fast Plugin before to use this shortcut.", MessageBox.TYPE_INFO)
			mybox.setTitle(_("Info"))		


	def NotYet(self):
		mybox = self.session.open(MessageBox, "Function Not Yet Available", MessageBox.TYPE_INFO)
		mybox.setTitle(_("Info"))


class DeliteSetupFp(Screen):
	skin = """
	<screen position="160,115" size="390,370" title="Black Hole Fast Plugin Setup">
		<widget source="list" render="Listbox" position="10,10" size="370,300" scrollbarMode="showOnDemand" >
			<convert type="StringList" />
		</widget>
		<ePixmap pixmap="skin_default/buttons/red.png" position="115,320" size="140,40" alphatest="on" />
		<widget name="key_red" position="115,320" zPosition="1" size="140,40" font="Regular;20" halign="center" valign="center" backgroundColor="#9f1313" transparent="1" />
	</screen>"""
	
	def __init__(self, session):
		Screen.__init__(self, session)
		
		self["key_red"] = Label(_("Set Favourite"))
		self.list = []
		self["list"] = List(self.list)
		self.updateList2()
		
		self["actions"] = ActionMap(["WizardActions", "ColorActions"],
		{
			"ok": self.save,
			"back": self.close,
			"red": self.save
		}, -1)
		
		
	def updateList2(self):
		self.list = [ ]
		self.pluginlist = plugins.getPlugins(PluginDescriptor.WHERE_PLUGINMENU)
		for plugin in self.pluginlist:
			#self.list.append(PluginEntryComponent(plugin))
			if plugin.icon is None:
				png = LoadPixmap(resolveFilename(SCOPE_SKIN_IMAGE, "skin_default/icons/plugin.png"))
			else:
				png = plugin.icon
			res = (plugin.name, plugin.description, png)
			self.list.append(res)
		
		self["list"].list = self.list
		
	def save(self):
		mysel = self["list"].getCurrent()
		if mysel:
			mysel = mysel[0]
			message = "Fast plugin set to: " + mysel + "\nKey: 2x Green"
			mybox = self.session.openWithCallback(self.close, MessageBox, message, MessageBox.TYPE_INFO)
			mybox.setTitle(_("Configuration Saved"))
			config.delite.fp.value = mysel
			config.delite.fp.save()
			configfile.save()



class DeliteGp:
	def __init__(self):
		self["DeliteGp"] = ActionMap( [ "InfobarSubserviceSelectionActions" ],
			{
				"DeliteGpshow": (self.showDeliteGp),
			})

	def showDeliteGp(self):
		self.session.openWithCallback(self.callNabAction, DeliteGreenPanel)

	def callNabAction(self, *args):
		if len(args):
			(actionmap, context, action) = args
			actionmap.action(context, action)