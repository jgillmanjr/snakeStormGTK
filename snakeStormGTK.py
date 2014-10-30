#!/usr/bin/env python
import snakeStorm
from gi.repository import Gtk



class init:
	""" The initial class to kick things off. """
	
	def __init__(self):
		self.connParams = {'username': 'user', 'password': 'pass', 'baseURI': 'https://api.stormondemand.com', 'apiPort': 443, 'verify': True, 'version': 'bleed'} # Initial
		self.availableVersions = (['v1'], ['bleed']) # Available API versions (will most likely be 'v1' and 'bleed' for a while..)

		self.gladeFile = 'snakeStormGTK.glade'
		self.builder = Gtk.Builder()
		self.builder.add_from_file(self.gladeFile)
		self.widgets = {}

		## Load widgets into dict {'widgetId': widgetObj}
		for x in self.builder.get_objects():
			self.widgets[Gtk.Buildable.get_name(x)] = x
		## End load widgets

		### Handlers ###
		self.handlers = {
			'openConnDialog':	self.openConnDialog,
			'quit':				self.quit,
			'hideWindow':		self.hideWindow,
			'saveConnDialog':	self.saveConnDialog,
			'testConn':			self.testConn
		}
		self.builder.connect_signals(self.handlers)
		### End Handlers ###

		### API Version Setup for the Connection Dialog combobox###
		self.widgets['versionStore'] = Gtk.ListStore(str)
		for x in self.availableVersions:
			self.widgets['versionStore'].append(x)
		self.widgets['versionCombo'].set_model(self.widgets['versionStore'])
		self.widgets['versionCell'] = Gtk.CellRendererText()
		self.widgets['versionCombo'].pack_start(self.widgets['versionCell'], True)
		self.widgets['versionCombo'].add_attribute(self.widgets['versionCell'], 'text', 0)
		###	End API Version Setup ###

		## Show the mainWindow ##
		self.widgets['mainWindow'].show()

		### Initial Storm Connection Stuff ###
		self.stormConn = snakeStorm.connection(**self.connParams)

	def hideWindow(self, *args, **kwargs):
		args[0].hide()

	def openConnDialog(self, *args, **kwargs):
		self.setupConnDialog()
		self.widgets['connDialog'].run()

	def getConnParams(self, *args, **kwargs):
		tempConnParams = {}
		versionIndex = self.widgets['versionCombo'].get_active()
		tempConnParams['username']	= self.widgets['userField'].get_text()
		tempConnParams['password']	= self.widgets['passField'].get_text()
		tempConnParams['baseURI']	= self.widgets['baseField'].get_text()
		tempConnParams['apiPort']	= int(self.widgets['portField'].get_text())
		tempConnParams['version']	= self.widgets['versionCombo'].get_model()[versionIndex][0]
		tempConnParams['verify']	= self.widgets['verifySwitch'].get_active()
		return tempConnParams
		del tempConnParams

	def saveConnDialog(self, *args, **kwargs):
		self.connParams = self.getConnParams()
		self.stormConn.changeBase(**self.connParams)

	def setupConnDialog(self):
		self.widgets['baseField'].set_text(self.stormConn.baseURI)
		self.widgets['portField'].set_text(str(self.stormConn.apiPort))
		self.widgets['userField'].set_text(self.stormConn.username)
		self.widgets['passField'].set_text(self.stormConn.password)
		if self.stormConn.version == 'v1': ## This is a fucking dirty way of doing it, but I can't think of a better way right now
			self.widgets['versionCombo'].set_active(0)
		else:
			self.widgets['versionCombo'].set_active(1)
		self.widgets['verifySwitch'].set_active(self.stormConn.verify)

	def testConn(self, *args, **kwargs):
		tempConnParams = self.getConnParams()
		self.stormConn.changeBase(**tempConnParams) # Change for the test
		test = snakeStorm.method('Utilities/Info/ping', self.stormConn)
		if 'snakeStormError' in test.request():
			self.widgets['messageDialog'].set_markup('<span size="xx-large" weight="ultrabold">There was an error.</span>')
			self.widgets['messageDialog'].format_secondary_text('There may be an error with either the API or snakeStorm - but it\'s most likely you have bad settings.')
		else:
			self.widgets['messageDialog'].set_markup('<span size="xx-large" weight="ultrabold">Success!</span>')
			self.widgets['messageDialog'].format_secondary_text('It appears things are working!')
		self.widgets['messageDialog'].set_transient_for(args[0])
		self.widgets['messageDialog'].set_title('Connection Test Result')
		self.widgets['messageDialog'].run()
		self.stormConn.changeBase(**self.connParams) # Change back after the test
		del test

	def main(self):
		Gtk.main()

	def quit(self, *args, **kwargs):
		Gtk.main_quit()

init = init()
init.main()
