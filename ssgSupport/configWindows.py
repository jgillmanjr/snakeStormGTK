"""
Contains the fuctions to build configuration dialogs, windows, and components
"""
from gi.repository import Gtk
import snakeStorm
import sptFunctions
mainObj = None # Placeholder until it gets populated

def buildListBox(comboWidgetName, listValues = None):
	"""
	This is for single column (string type) combo box. The box should already exist.
	* comboWidgetName: The name of the comboBox widget that you are building out
	* listValues: If passed in, they will be added to the list store
	"""
	comboName	= comboWidgetName
	storeName	= comboWidgetName + 'Store'
	cellName	= comboWidgetName + 'Cell'
	
	mainObj.widgets[storeName]	= Gtk.ListStore(str)
	mainObj.widgets[cellName]	= Gtk.CellRendererText()

	mainObj.widgets[comboName].set_model(mainObj.widgets[storeName])
	mainObj.widgets[comboName].pack_start(mainObj.widgets[cellName], True)
	mainObj.widgets[comboName].add_attribute(mainObj.widgets[cellName], 'text', 0)

	if listValues is not None:
		for x in listValues:
			mainObj.widgets[storeName].append(x)

