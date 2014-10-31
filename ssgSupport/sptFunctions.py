"""
Supporting Functions
"""
from gi.repository import Gtk
import snakeStorm
mainObj = None # Placeholder until it gets populated

def getConnParams(*args, **kwargs):
	""" Get the connection parameters from the config dialog. """
	tempConnParams = {}
	versionIndex = mainObj.widgets['versionCombo'].get_active()
	tempConnParams['username']	= mainObj.widgets['userField'].get_text()
	tempConnParams['password']	= mainObj.widgets['passField'].get_text()
	tempConnParams['baseURI']	= mainObj.widgets['baseField'].get_text()
	tempConnParams['apiPort']	= int(mainObj.widgets['portField'].get_text())
	tempConnParams['version']	= mainObj.widgets['versionCombo'].get_model()[versionIndex][0]
	tempConnParams['verify']	= mainObj.widgets['verifySwitch'].get_active()
	return tempConnParams
	del tempConnParams

def setupConnDialog():
	""" Populate the connection configuration fields. """
	mainObj.widgets['baseField'].set_text(mainObj.stormConn.baseURI)
	mainObj.widgets['portField'].set_text(str(mainObj.stormConn.apiPort))
	mainObj.widgets['userField'].set_text(mainObj.stormConn.username)
	mainObj.widgets['passField'].set_text(mainObj.stormConn.password)
	if mainObj.stormConn.version == 'v1': ## This is a fucking dirty way of doing it, but I can't think of a better way right now
		mainObj.widgets['versionCombo'].set_active(0)
	else:
		mainObj.widgets['versionCombo'].set_active(1)
	mainObj.widgets['verifySwitch'].set_active(mainObj.stormConn.verify)
