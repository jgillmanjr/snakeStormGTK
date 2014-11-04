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

def buildListStore(storeName, values = None):
	"""
	This is to build a single column ListStore independent of anything else. Strings only, plz.
	* storeName: The name of the store. Careful - will overwrite if existing already.
	* values: A list or set of values to insert - if passed in.
	"""
	mainObj.widgets[storeName] = Gtk.ListStore(str)
	if values is not None:
		for x in values:
			mainObj.widgets[storeName].append([x])


def buildAutoComplete(valueStore, entryName):
	"""
	This is to build an EntryCompletion widget based off an existing single column list store. If entryName is already in use, that widget will be used instead of creating a new one.
	* valueStore: The name of the value store you want to use.
	* entryName: The name of the entry widget.
	"""
	completeName	= entryName + 'Completion'
	if entryName not in mainObj.widgets: # Create a new entry object
		mainObj.widgets[entryName] = Gtk.Entry()

	mainObj.widgets[completeName]	= Gtk.EntryCompletion()
	mainObj.widgets[completeName].set_model(mainObj.widgets[valueStore])

	mainObj.widgets[entryName].set_completion(mainObj.widgets[completeName])
	mainObj.widgets[completeName].set_text_column(0)

	## Debug below ##
	w = mainObj.widgets

def buildResultTreeView():
	"""
	Build out the treeview of the results
	"""
	mainObj.widgets['resultStore']	= Gtk.TreeStore(str)
	mainObj.widgets['resultCellRenderer'] = Gtk.CellRendererText()
	mainObj.widgets['resultColumn'] = Gtk.TreeViewColumn('Data', mainObj.widgets['resultCellRenderer'], text=0)
	mainObj.widgets['resultView']	= Gtk.TreeView(mainObj.widgets['resultStore'])
	mainObj.widgets['resultView'].append_column(mainObj.widgets['resultColumn'])
	mainObj.widgets['resultScroll'].add(mainObj.widgets['resultView'])
	mainObj.widgets['resultView'].show_now()

def buildTreeStore(store, values):
	"""
	Build out a single column tree store. MultiLevel support.
	* store: The store. Will clear and overwrite - which is useful for some things like API results.
	* values: The data.
	"""

	def is_scalar (value):
		""" Convenience for the iterToStor function. """
		return isinstance(value,(type(None),str,int,float,bool,unicode))

	def iterToStore(iterable, inPiter = None):
		""" Does the actual addition to the store. Concats the key and value if value is a scalar. """
		if type(iterable) is dict:
			for k, v in iterable.iteritems():
				if is_scalar(v):
					appendValue = k + ': ' + str(v)
					piter = store.append(inPiter, [appendValue])
				else:
					appendValue = k + ':'
					piter = store.append(inPiter, [appendValue])
					iterToStore(v, piter)
		else: # list, set, etc
			for i, v in enumerate(iterable):
				if is_scalar(v):
					piter = store.append(inPiter, [v])
				else:
					appendValue = '[' + str(i) + ']'
					piter = store.append(inPiter, [appendValue])
					iterToStore(v, piter)

	store.clear()

	iterToStore(values)
