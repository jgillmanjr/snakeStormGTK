"""
Contains the fuctions to build configuration dialogs, windows, and components
"""
from gi.repository import Gtk
import snakeStorm
import sptFunctions
mainObj = None # Placeholder until it gets populated

def buildListBox(comboWidgetName, listValues = None, valueStore = None):
	"""
	This is for single column (string type) combo box. The box should already exist.
	* comboWidgetName: The name of the comboBox widget that you are building out
	* listValues: If passed in, they will be added to the list store if it is a new one
	* valueStore: The name of an existing value store you want to use. If not passed in, a new one will be created
	"""
	comboName	= comboWidgetName
	cellName	= comboWidgetName + 'Cell'

	mainObj.widgets[cellName]	= Gtk.CellRendererText()

	if valueStore is None: # New Value Store - not reusing
		storeName	= comboWidgetName + 'Store'
		mainObj.widgets[storeName]	= Gtk.ListStore(str)		

		if listValues is not None: # This obviously only runs for new valueStores
			for x in listValues:
				mainObj.widgets[storeName].append([x])
	else:
		storeName	= valueStore

	mainObj.widgets[comboName].set_model(mainObj.widgets[storeName])
	mainObj.widgets[comboName].pack_start(mainObj.widgets[cellName], True)
	mainObj.widgets[comboName].add_attribute(mainObj.widgets[cellName], 'text', 0)

	

