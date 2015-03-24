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

def is_scalar (value):
	""" Convenience for the iterToStor functions. """
	return isinstance(value,(type(None),str,int,float,bool,unicode))

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
	w = mainObj.widgets

	w['resultStore']	= Gtk.TreeStore(str)
	w['resultCellRenderer'] = Gtk.CellRendererText()
	w['resultColumn'] = Gtk.TreeViewColumn('Data', w['resultCellRenderer'], text=0)
	w['resultView']	= Gtk.TreeView(w['resultStore'])
	w['resultView'].append_column(w['resultColumn'])
	w['resultScroll'].add(w['resultView'])
	w['resultView'].show_now()

def buildTreeStore(store, values):
	"""
	Build out a single column tree store. MultiLevel support.
	* store: The store. Will clear and overwrite - which is useful for some things like API results.
	* values: The data.
	"""

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

def buildParamTreeView():
	"""
	Build out the TreeView for API parameters
	"""
	w = mainObj.widgets

	w['paramStore'] = Gtk.TreeStore(str, str, bool)
	
	w['paramCellKey'] = Gtk.CellRendererText(editable = True)
	w['paramCellValue'] = Gtk.CellRendererText(editable = True)
	w['paramCellUse'] = Gtk.CellRendererToggle(activatable = True)

	w['paramColumnKey'] = Gtk.TreeViewColumn('Param Key', w['paramCellKey'], text=0)
	w['paramColumnKey'].set_alignment(0.5)
	w['paramColumnValue'] = Gtk.TreeViewColumn('Param Value', w['paramCellValue'], text=1)
	w['paramColumnValue'].set_alignment(0.5)
	w['paramColumnUse'] = Gtk.TreeViewColumn('Use Param/Value', w['paramCellUse'], active=2)
	w['paramColumnUse'].set_alignment(0.5)

	w['paramView'] = Gtk.TreeView(w['paramStore'])
	w['paramView'].append_column(w['paramColumnKey'])
	w['paramView'].append_column(w['paramColumnValue'])
	w['paramView'].append_column(w['paramColumnUse'])

	w['paramScroll'].add(w['paramView'])

	w['paramView'].show_now()

def buildParamTreeStore(methodName):
	""" Build the Parameter Store. """
	def valueEdited(*args, **kwargs):
		""" What do if the value cell is edited. """
		editIter = w['paramStore'].get_iter_from_string(args[1])
		w['paramStore'].set_value(editIter, 1, args[2])

	def keyEdited(*args, **kwargs):
		""" What do if the key cell is edited. """
		editIter = w['paramStore'].get_iter_from_string(args[1])
		w['paramStore'].set_value(editIter, 0, args[2])

	def toggleCheck(*args, **kwargs):
		""" Toggle the use checkbox. """
		w['paramStore'][args[1]][2] = not w['paramStore'][args[1]][2]

	def addChild(*args, **kwargs):
		""" Add a child row. """
		piter = w['paramStore'].get_iter(args[1])
		w['paramStore'].append(piter, ['', 'Value Here', False])

	def iterToStore(iterable, inPiter = None):
		""" Does the actual addition to the store. """
		if type(iterable) is dict:
			for k, v in iterable.iteritems():
				if is_scalar(v):
					appendValue = [k, str(v), False]
					piter = w['paramStore'].append(inPiter, appendValue)
				else:
					appendValue = [k, '-----', False]
					piter = w['paramStore'].append(inPiter, appendValue)
					iterToStore(v, piter)
		else: # list, set, etc
			for v in iterable:
				if is_scalar(v):
					piter = w['paramStore'].append(inPiter, ['', str(v), False])
				else:
					appendValue = ['', '-----', False]
					piter = w['paramStore'].append(inPiter, appendValue)
					iterToStore(v, piter)


	w = mainObj.widgets

	w['paramCellValue'].connect('edited', valueEdited)
	w['paramCellKey'].connect('edited', keyEdited)
	w['paramCellUse'].connect('toggled', toggleCheck)
	#w['paramView'].connect('row-activated', addChild) ### Disabled until I can get params to even save..

	w['paramStore'].clear()

	apiMethod = mainObj.apiMethods[methodName]
	for k, v in apiMethod.inputParams().iteritems(): # Generate the params, and populate values if already set for the method
		initValue = {}
		if k in apiMethod.listParams():
			initValue['value'] = apiMethod.listParams()[k]
			initValue['flag'] = True
		else:
			initValue['value'] = 'Value Here'
			initValue['flag'] = False
		w['paramStore'].append(None, [k, initValue['value'], initValue['flag']])
