"""
GTK Signal Handling Operations Go Here
"""
from gi.repository import Gtk
import snakeStorm
import sptFunctions
mainObj = None # Placeholder until it gets populated

def hideWindow(*args, **kwargs):
	""" Hide a window or dialog. """
	args[0].hide()
	return True # Prevents windows from being destroyed

def addMethod(*args, **kwargs):
	""" Add a method to the combobox. """
	addValue = [args[0].get_text()]
	mainObj.widgets['methodComboStore'].append(addValue)

def clearEntry(*args, **kwargs):
	""" Clear an entry field. """
	args[0].set_text('')

def openConnDialog(*args, **kwargs):
	""" Open the Connection settings dialog. """
	sptFunctions.setupConnDialog()
	mainObj.widgets['connDialog'].run()

def saveConnDialog(*args, **kwargs):
	""" Save the connection Settings. """
	mainObj.connParams = sptFunctions.getConnParams()
	mainObj.stormConn.changeBase(**mainObj.connParams)

def testConn(*args, **kwargs):
	""" Test the connection settings as entered. """
	tempConnParams = sptFunctions.getConnParams()
	mainObj.stormConn.changeBase(**tempConnParams) # Change for the test
	test = snakeStorm.method('Utilities/Info/ping', mainObj.stormConn)
	if 'snakeStormError' in test.request():
		mainObj.widgets['messageDialog'].set_markup('<span size="xx-large" weight="ultrabold">There was an error.</span>')
		mainObj.widgets['messageDialog'].format_secondary_text('There may be an error with either the API or snakeStorm - but it\'s most likely you have bad settings.')
	else:
		mainObj.widgets['messageDialog'].set_markup('<span size="xx-large" weight="ultrabold">Success!</span>')
		mainObj.widgets['messageDialog'].format_secondary_text('It appears things are working!')
	mainObj.widgets['messageDialog'].set_transient_for(args[0])
	mainObj.widgets['messageDialog'].set_title('Connection Test Result')
	mainObj.widgets['messageDialog'].run()
	mainObj.stormConn.changeBase(**mainObj.connParams) # Change back after the test
	del test

def openMethodDialog(*args, **kwargs):
	""" Open the new method dialog. """
	mainObj.widgets['newMethod'].run()

def showWindow(*args, **kwargs):
	""" Run a dialog or show a window. """
	try:
		args[0].run()
	except AttributeError: # Regular windows don't have run
		args[0].show()