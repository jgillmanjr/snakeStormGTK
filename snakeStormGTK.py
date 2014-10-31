#!/usr/bin/env python
import snakeStorm
from gi.repository import Gtk
from ssgSupport import *



class main:
	""" The initial class to kick things off. """
	
	def __init__(self):
		### Initial Storm Connection Stuff ###
		self.connParams = {'username': 'user', 'password': 'pass', 'baseURI': 'https://api.stormondemand.com', 'apiPort': 443, 'verify': True, 'version': 'bleed'} # Initial
		self.stormConn = snakeStorm.connection(**self.connParams)
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
			'openConnDialog':	sigHandlers.openConnDialog,
			'quit':				self.quit,
			'hideWindow':		sigHandlers.hideWindow,
			'saveConnDialog':	sigHandlers.saveConnDialog,
			'testConn':			sigHandlers.testConn,
			'addMethod':		sigHandlers.addMethod,
			'openMethodDialog':	sigHandlers.openMethodDialog,
			'clearEntry':		sigHandlers.clearEntry,
			'showWindow':		sigHandlers.showWindow
		}
		self.builder.connect_signals(self.handlers)
		### End Handlers ###

	def finalSetup(self):
		""" Complete setup that needs to occur after emitting the main object to the required modules. """
		### Combobox Setup###
		configWindows.buildListBox('versionCombo', listValues = self.availableVersions) # API Version Combobox
		configWindows.buildListBox('methodCombo') # API Method Combobox
		configWindows.buildListBox('methodSelector', valueStore = 'methodComboStore')

		sigHandlers.showWindow(self.widgets['mainWindow']) # Show the main window

	def main(self):
		""" Start. """
		Gtk.main()

	def quit(self, *args, **kwargs):
		""" Stop. """
		Gtk.main_quit()

	

init = main()

for module in [sigHandlers, sptFunctions, configWindows]:
	module.mainObj = init # pass along the object to the specified modules so they can do the needful
init.finalSetup()
init.main()
