"""
GTK Signal Handling Operations Go Here
"""
from gi.repository import Gtk
import snakeStorm
import sptFunctions
import configWindows
mainObj = None # Placeholder until it gets populated

def hideWindow(*args, **kwargs):
	""" Hide a window or dialog. """
	args[0].hide()
	return True # Prevents windows from being destroyed

def clearEntry(*args, **kwargs):
	""" Clear an entry field. """
	args[0].set_text('')

def openConnDialog(*args, **kwargs):
	""" Open the Connection settings dialog. """
	sptFunctions.setupConnDialog()
	mainObj.widgets['connDialog'].run()

def regenMethodList(*args, **kwargs):
	mainObj.widgets['apiMethodList'].clear()
	mainObj.apiMethods.clear()
	for x in snakeStorm.listApiMethods(mainObj.stormConn.version):
		mainObj.widgets['apiMethodList'].append([x])
		mainObj.apiMethods[x.lower()] = snakeStorm.method(x, mainObj.stormConn)

def makeRequest(*args, **kwargs):
	""" Make the API request and return the result. """
	apiMethod = args[0].get_text().lower()
	if apiMethod in mainObj.apiMethods:
		configWindows.buildTreeStore(mainObj.widgets['resultStore'], mainObj.apiMethods[apiMethod].request())

def hideBtnImg(*args, **kwargs):
	""" Hide the image on a button. """
	args[0].get_image().hide()

def showBtnImg(*args, **kwargs):
	""" Show the image on a button. """
	args[0].get_image().show()

def showParamsDialog(*args, **kwargs):
	""" Show the parameter dialog. """
	apiMethod = args[0].get_text().lower()
	if apiMethod in mainObj.apiMethods and len(mainObj.apiMethods[apiMethod].inputParams()) > 0:
		mainObj.widgets['methodLabel'].set_text(args[0].get_text())
		configWindows.buildParamTreeStore(apiMethod)
		mainObj.widgets['paramsDialog'].set_title('Method Parameters: ' + args[0].get_text())
		mainObj.widgets['paramsDialog'].show()

def saveConnDialog(*args, **kwargs):
	""" Save the connection Settings. """
	mainObj.connParams = sptFunctions.getConnParams()
	mainObj.stormConn.changeBase(**mainObj.connParams)

def saveParams(*args, **kwargs):
	""" Save the parameters for the currently active method. """
	apiMethod = args[0].get_text().lower()
	
	def treeToDict(store, treeiter):
		"""
		Process the tree to get parameter components, and ultimately the whole set.
		Row Index 0: Key
		Row Index 2: Value 
		"""
		while treeiter != None:
			# Determine if returning a dict or a listValue to thisLevelData. #
			# If thisLevelData has not been defined yet, define it to the type that matches first.#
			# If type match doesn't happen, well, whupz, you get an error. I should make it pop a dialog. #
			key = store[treeiter][0]
			if key == '':
				if 'thisLevelData' not in locals():
					thisLevelData = []
				isListVal = True
			else:
				if 'thisLevelData' not in locals():
					thisLevelData = {}
				isListVal = False

			# If no children, take the value set in the row #
			if store.iter_has_child(treeiter):
				childiter = store.iter_children(treeiter)
				value = treeToDict(store, childiter)
			else:
				value = store[treeiter][1]

			if isListVal:
				thisLevelData.append(value)
			else:
				thisLevelData[key] = value

			treeiter = store.iter_next(treeiter)

		return thisLevelData
	
	store = mainObj.widgets['paramStore']
	initIter = mainObj.widgets['paramStore'].get_iter_first()
	methodObj = mainObj.apiMethods[apiMethod]
	apiParams = treeToDict(store, initIter)

	methodObj.addParams(**apiParams)

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

def showWindow(*args, **kwargs):
	""" Run a dialog or show a window. """
	try:
		args[0].run()
	except AttributeError: # Regular windows don't have run
		args[0].show()
