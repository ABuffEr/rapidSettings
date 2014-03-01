# -*- coding: UTF-8 -*-
# Author: Alberto buffolino
import globalPluginHandler
import wx
import gui
from gui.settingsDialogs import *
import config
from msg import message as msg
import queueHandler
import ui
from tones import beep
from logHandler import log
import addonHandler
addonHandler.initTranslation()

_addonDir = os.path.join(os.path.dirname(__file__), "..", "..").decode("mbcs")
_curAddon = addonHandler.Addon(_addonDir)
_addonSummary = _curAddon.manifest['summary']
_scriptCategory = unicode(_addonSummary)

# the global variable to store current settings dialog instance
ins = None

class SettingsTree(wx.TreeCtrl):
	"""Class that implement all operation on the tree"""

	# list of tuples (settings section, relative class dialog to instantiate)
	classList = [
		# Translators: name for General settings
		(_("General"), GeneralSettingsDialog),
		(msg("Synthesizer"), SynthesizerDialog),
		(msg("&Voice"), VoiceSettingsDialog),
		(msg("Braille"), BrailleSettingsDialog),
		# Translators: name for Keyboard settings
		(_("Keyboard"), KeyboardSettingsDialog),
		(msg("Mouse"), MouseSettingsDialog),
		(msg("Review &cursor...").replace('...', ''), ReviewCursorDialog),
		# Translators: name for Input Composition settings
		(_("Input Composition"), InputCompositionDialog),
		(msg("Object Presentation"), ObjectPresentationDialog),
		(msg("Browse Mode"), BrowseModeDialog),
		(msg("Document Formatting"), DocumentFormattingDialog)
	]
	# string to store term entered in search field, default blank
	find = ""

	def __init__(self, *args, **kwargs):
		super(SettingsTree, self).__init__(*args, style=wx.TR_HIDE_ROOT, **kwargs)
		self.Bind(wx.EVT_TREE_ITEM_EXPANDING, self.onExpandingItem)
		self.Bind(wx.EVT_TREE_ITEM_COLLAPSED, self.onCollapsedItem)
		# a variable to check if there is a section expanded
		self._expanded = False
		self.root = self.AddRoot("")
		self.SetItemHasChildren(self.root)
		self.initSections(self.classList)

	def initSections(self, classList):
		"""Add to the tree the sections specified in classList parameter"""
		# clean the tree (eventually modified by a search)
		self.DeleteChildren(self.root)
		for item in classList:
			# create a tree item and associate it with the section name
			treeSubItem = self.AppendItem(self.root, item[0])
			self.SetItemHasChildren(treeSubItem)
			# associate also with the relative class
			self.SetPyData(treeSubItem, item[1])

	def onExpandingItem(self, event):
		"""Populate the section tree item with various options in this section"""
		if self._expanded:
			# collapse the expanded section, generating a wx.EVT_TREE_ITEM_COLLAPSED event
			self.CollapseAll()
		self._expanded = True
		treeItem = event.GetItem()
		classDialog = self.GetPyData(treeItem)
		global ins
		# instantiate the settings section dialog
		ins = classDialog(self)
		# workaround: show to then immediately hide the dialog, that is our phantom slave, now :-)
		ins.Show()
		ins.Hide()
		# list of all wx controls in the dialog
		children = ins.GetChildren()
		# loop to prepare names for tree items, based on combobox, editbox, checkbox and slider
		for n in range(0,len(children)):
			child = children[n]
			name = None
			if child.IsEnabled():
				if child.ClassName == u'wxChoice':
					# some combobox has a name, a brief version of the relative staticText label...
					if child.GetName() != 'choice':
						# the colon presence is very inconsistent
						sep = ' ' if child.GetName().endswith(':') else ': '
						# concatenate name, separator and current value of combobox
						name = sep.join([msg(child.GetName()), msg(child.GetLabel())])
					else:
						# ...but some other has "choice" as name, so we take the staticText label, the previous control
						sep = ' ' if children[n-1].GetLabel().endswith(':') else ': '
						name = sep.join([msg(children[n-1].GetLabel()), msg(child.GetLabel())])
				elif child.ClassName == u'wxTextCtrl':
					name = ': '.join([msg(children[n-1].GetLabel()), child.GetLabel()])
				elif child.ClassName == u'wxCheckBox':
					name = ': '.join([msg(child.GetLabel()), msg("on" if child.GetValue() else "off")])
				elif child.ClassName == u'wxSlider':
					name = ' '.join([msg(child.GetName()), str(child.GetValue())+'%'])
			# if name is None then child is probably a button, so we ignore it;
			# if self.find is blank, it's automatically present in all not None names
			if name is not None and self.find in name.lower():
				treeSubItem = self.AppendItem(treeItem, name)
				self.Bind(wx.EVT_TREE_SEL_CHANGED, self.onSelectedItem)
				self.Bind(wx.EVT_KEY_DOWN, self.onSpacePress)
				self.Bind(wx.EVT_KEY_UP, self.onExit)
				# associate tree item with relative control
				self.SetPyData(treeSubItem, child)

	def onCollapsedItem(self, event):
		"""Collapse and reset the section tree item, call saveAlert in SettingsTreeDialog"""
		item = event.GetItem()
		self.CollapseAndReset(item)
		self.SetItemHasChildren(item)
		self.GetParent().saveAlert(self.GetItemText(item))
		self._expanded = False

	def onSelectedItem(self, event):
		"""Call enableItem in SettingsTreeDialog, control associated with tree item as parameter"""
		item = event.GetItem()
		# a wx control in original settings dialog: checkbox, editbox, etc
		wxControl = self.GetPyData(item)
		self.GetParent().enableItem(wxControl)

	def onSpacePress(self, event):
		"""Call cycleItem in SettingsTreeDialog, control associated with tree item as parameter"""
		if event.GetKeyCode() == wx.WXK_SPACE:
			item = self.GetSelection()
			wxControl = self.GetPyData(item)
			self.GetParent().cycleItem(wxControl)
		else:
			event.Skip()

	def onExit(self, event):
		"""Invoke Destroy method of parent if you press escape"""
		if event.GetKeyCode() == wx.WXK_ESCAPE:
			self.GetParent().Destroy()
		else:
			event.Skip()

	def updateLabel(self, curValue, suffix=""):
		"""Update text representation of current wx control in the tree"""
		curTreeItem = self.GetSelection()
		curName = self.GetItemText(curTreeItem)
		baseName = curName.rsplit(': ', 1)[0]
		# suffix is '%' if current wx control is a slider, blank otherwise
		newName = ': '.join([baseName, msg(curValue)+suffix])
		self.SetItemText(curTreeItem, newName)

	def search(self, input):
		"""Search the specified string in all tree items name"""
		# if input is blank, rebuild the original tree
		if input == "":
			self.find = input
			self.initSections(self.classList)
			self.SetFocus()
			return
		# put input in lowercase
		input = input.lower()
		if self._expanded:
			self.CollapseAll()
		# list of class dialogs that have at least a wx control matching  the search
		matchingClasses = []
		# two variables for beep progress
		n = 0
		p = float(100.0)
		for item in self.classList:
			# see behaviors.py in NVDA source for original formula
			beep(110*2**(n*p/10/25.0), 40)
			classDialog = item[1]
			global ins
			ins = classDialog(self)
			ins.Show()
			ins.Hide()
			for child in ins.GetChildren():
				# exclude buttons
				if child.ClassName != 'wxButton':
					# list that collects name and label attribute of control
					l = [child.GetName(), child.GetLabel()]
					# if control has also GetValue method...
					if 'GetValue' in dir(child):
						# if it's a checkbox...
						if child.GetValue() in [True, False]:
							# ...append to the list "on" and "off" NVDA translation
							l.append(msg("on") if child.GetValue() else msg("off"))
						# ...else, if it's a slider, or editbox...
						else:
							# ...append to the list the value string representation
							l.append(str(child.GetValue()))
					# finally, check if there is at least one occurrence of input in control attributes in lowercase and without symbol "&"
					if len(filter(lambda f: input in f.lower().replace('&', ''), l))>0:
						# if yes, this class dialog is good for us
						matchingClasses.append(item)
						# break the loop on controls, one in each class is sufficient
						break
			# checking on its controls is finished, so destroy phantom dialog
			ins.Destroy()
			# force _hasInstance to False, while phantom dialog is destroying, to bypass MultiInstanceError
			SettingsDialog._hasInstance = False
			n += 1
		# if there is no result...
		if len(matchingClasses) == 0:
			# announce input not found
			queueHandler.queueFunction(queueHandler.eventQueue, ui.message, msg("text \"%s\" not found")%input)
		# ...rebuild and focalize the tree and expand first section, otherwise
		else:
			# rebuild tree with chosen classes/sections
			self.initSections(matchingClasses)
			# setting self.find to input, expansion can work correctly
			self.find = input
			self.SetFocus()
			firstItem = self.GetFirstVisibleItem()
			self.Expand(firstItem)

class SettingsTreeDialog(SettingsDialog):
	"""Class that implements main dialog"""

	# blank title, set in init
	title = ""

	def __new__(cls, *args, **kwargs):
		"""New method, to extend SettingsDialog and use its elements, bypassing multi instance limitation"""
		# if there is already a SettingsDialog subclass instantiated,
		# you'll not be able to expand any section on the tree
		if SettingsDialog._hasInstance:
			# so, alert and not instantiate this dialog
			gui.messageBox(msg("An NVDA settings dialog is already open. Please close it first."), msg("Error"), style=wx.OK | wx.ICON_ERROR)
		else:
			obj = super(SettingsDialog, cls).__new__(cls, *args, **kwargs)
			return obj

	def __init__(self, *args, **kwargs):
		"""Init method, it sets title according to active profiles"""
		# We remove profile 0, the first one, which is the normal profile, always active.
		activeProfiles = config.conf.profiles[1:]
		profileNames = []
		profileTitle = ''
		while len(activeProfiles) > 0:
			profileNames.append(activeProfiles.pop().name)
		if len(profileNames)>0:
			profileTitle = '('+', '.join(profileNames)+')'
		self.title = ' '.join([_addonSummary, profileTitle])
		super(SettingsTreeDialog, self).__init__(*args, **kwargs)

	def makeSettings(self, settingsSizer):
		"""Create and add all necessary wx controls"""
		searchLabel = wx.StaticText(self, wx.NewId(), label=msg("search").capitalize()+":")
		settingsSizer.Add(searchLabel)
		self.search = wx.TextCtrl(self, wx.NewId(), style=wx.TE_PROCESS_ENTER)
		self.search.Bind(wx.EVT_TEXT_ENTER, self.onInputSearch)
		settingsSizer.Add(self.search)
		sizer = wx.BoxSizer(wx.VERTICAL)
		self.tree = SettingsTree(self)
		sizer.Add(self.tree)
		settingsSizer.Add(sizer)
		sizer = wx.BoxSizer(wx.HORIZONTAL)
		self.combo = wx.Choice(self, wx.NewId())
		sizer.Add(self.combo)
		self.edit = wx.TextCtrl(self, wx.NewId())
		sizer.Add(self.edit)
		self.rb1 = wx.RadioButton(self, wx.NewId(), label=msg("on"), style=wx.RB_GROUP)
		sizer.Add(self.rb1)
		self.rb2 = wx.RadioButton(self, wx.NewId(), label=msg("off"))
		sizer.Add(self.rb2)
		self.slider = wx.Slider(self, wx.ID_ANY, minValue=0, maxValue=100)
		sizer.Add(self.slider)
		settingsSizer.Add(sizer)
		self.disableAll()
		self.changedItems = []

	def postInit(self):
		"""Focalize the tree"""
		self.tree.SetFocus()

	def disableAll(self):
		"""Disable all controls, except search field and its label"""
		for item in [self.combo, self.edit, self.rb1, self.rb2, self.slider]:
			item.Disable()

	def enableItem(self, item):
		"""Switch to correct enable method according to item passed type (item is a wx control of phantom dialog)"""
		self.disableAll()
		if item.ClassName == u'wxChoice':
			self.enableCombo(item)
		elif item.ClassName == u'wxTextCtrl':
			self.enableEdit(item)
		elif item.ClassName == u'wxCheckBox':
			self.enableRB(item)
		elif item.ClassName == u'wxSlider':
			self.enableSlider(item)

	def enableCombo(self, combo):
		"""Set and enable combobox"""
		self.combo.SetItems(combo.GetItems())
		# a variable to then check if there was a change or not
		self.comboOriginalSelection = combo.GetSelection()
		self.combo.SetSelection(self.comboOriginalSelection)
		self.combo.Bind(wx.EVT_CHOICE, lambda event, item=combo: self.onItemChange(event, item))
		self.combo.Enable()

	def enableEdit(self, edit):
		"""Set and enable editbox"""
		# unbind to prevent a premature onItemChange execution, caused by SetValue
		self.edit.Unbind(wx.EVT_TEXT)
		self.editOriginalValue = edit.GetValue()
		self.edit.SetValue(self.editOriginalValue)
		self.edit.Bind(wx.EVT_TEXT, lambda event, item=edit: self.onItemChange(event, item))
		self.edit.Enable()

	def enableRB(self, chk):
		"""Set and enable radio button"""
		self.chkOriginalValue = chk.GetValue()
		if chk.GetValue():
			self.rb1.SetValue(True)
			self.rb2.SetValue(False)
		else:
			self.rb1.SetValue(False)
			self.rb2.SetValue(True)
		self.rb1.Bind(wx.EVT_RADIOBUTTON, lambda event, item=chk: self.onItemChange(event, item))
		self.rb2.Bind(wx.EVT_RADIOBUTTON, lambda event, item=chk: self.onItemChange(event, item))
		self.rb1.Enable()
		self.rb2.Enable()

	def enableSlider(self, slider):
		"""Set and enable slider"""
		self.sliderOriginalValue = slider.GetValue()
		self.slider.SetValue(slider.GetValue())
		self.slider.Bind(wx.EVT_COMMAND_SCROLL, lambda event, item=slider: self.onItemChange(event, item))
		self.slider.Enable()

	def onInputSearch(self, event):
		"""Process input in search field, call search method on the tree"""
		input = self.search.GetValue()
		self.search.SetValue("")
		self.search.Refresh()
		self.tree.search(input)

	def onItemChange(self, event, item):
		"""Manage changes in this dialog controls and in phantom dialog"""
		# if phantom control is not present in changedItems...
		if item not in self.changedItems:
			# ...add it, to default
			self.changedItems.append(item)
		if item.ClassName == u'wxChoice':
			# but if no real change is occurred...
			if self.combo.GetSelection() == self.comboOriginalSelection:
				# ...remove phantom control from changedItems
				self.changedItems.remove(item)
			# syncronize two combobox, anyway
			item.SetSelection(self.combo.GetSelection())
			# force phantom combobox to process its event method,
			# useful for language and variant comboboxes in voice section
			item.GetEventHandler().ProcessEvent(event)
			# request a update to relative tree item
			self.tree.updateLabel(self.combo.GetLabel())
		elif item.ClassName == u'wxTextCtrl':
			if self.edit.GetValue() == self.editOriginalValue:
				self.changedItems.remove(item)
			item.SetValue(self.edit.GetValue())
			self.tree.updateLabel(self.edit.GetValue())
		elif item.ClassName == u'wxCheckBox':
			# more complicated: check what radio button is enabled, and if enabled one has the original value
			if (self.chkOriginalValue and self.rb1.GetValue()) or (not self.chkOriginalValue and self.rb2.GetValue()):
				self.changedItems.remove(item)
			item.SetValue(True if self.rb1.GetValue() else False)
			self.tree.updateLabel("on" if self.rb1.GetValue() else "off")
		elif item.ClassName == u'wxSlider':
			if self.sliderOriginalValue == item.GetValue():
				self.changedItems.remove(item)
			item.SetValue(self.slider.GetValue())
			self.tree.updateLabel(str(self.slider.GetValue()), suffix='%')

	def cycleItem(self, item):
		if item.ClassName == u'wxChoice':
			nextSelection = self.combo.GetSelection()+1
			if nextSelection == len(self.combo.GetItems()):
				nextSelection = 0
			self.combo.SetSelection(nextSelection)
			# entire life is a workaround...
			event = wx.CommandEvent(wx.wxEVT_COMMAND_CHOICE_SELECTED)
			event.SetInt(self.combo.GetSelection())
			self.onItemChange(event, item)
		elif item.ClassName == u'wxTextCtrl':
			if not self.edit.GetValue().isdigit():
				self.edit.SetFocus()
			else:
				nextValue = int(self.edit.GetValue())+1
				self.edit.SetValue(str(nextValue))
				# except for combobox, event is not really necessary
				self.onItemChange(None, item)
		elif item.ClassName == u'wxCheckBox':
			if self.rb1.GetValue():
				self.rb1.SetValue(False)
				self.rb2.SetValue(True)
			else:
				self.rb1.SetValue(True)
				self.rb2.SetValue(False)
			self.onItemChange(None, item)
		if item.ClassName == u'wxSlider':
			nextValue = self.slider.GetValue()+1
			if nextValue == self.slider.GetMax()+1:
				nextValue = 0
			self.slider.SetValue(nextValue)
			self.onItemChange(None, item)

	def onOk(self, event):
		"""Call onOk(event) on phantom dialog instance, if this exists, and the same on superclass"""
		if ins is not None and "wxPyDeadObject" not in str(ins.__class__):
			ins.onOk(event)
		super(SettingsTreeDialog, self).onOk(event)

	def onCancel(self, event):
		"""Call onCancel(event) on phantom dialog instance, if this exists, and the same on superclass"""
		if ins is not None and "wxPyDeadObject" not in str(ins.__class__):
			ins.onCancel(event)
		super(SettingsTreeDialog, self).onCancel(event)

	def saveAlert(self, section):
		"""Alert to ask if you want to save changes"""
		if len(self.changedItems) == 0:
			ins.Destroy()
			# force _hasInstance to False, while phantom dialog is destroying, to bypass MultiInstanceError
			SettingsDialog._hasInstance = False
			return
		if gui.messageBox(
			# Translators: the message for save changes
			_("Do you want to save changes for {section} section?").format(section=section), msg("Warning"), wx.YES | wx.NO | wx.ICON_WARNING, self
			) == wx.YES:
			ins.onOk(wx.EVT_BUTTON)
		else:
			ins.onCancel(wx.EVT_BUTTON)
		# force _hasInstance to False, while phantom dialog is destroying after onOk or onCancel execution, to bypass MultiInstanceError
		SettingsDialog._hasInstance = False
		# reset changedItems list
		self.changedItems = []

class GlobalPlugin(globalPluginHandler.GlobalPlugin):

	scriptCategory = _scriptCategory

	def script_showSettingsTree(self, gesture):
		def run():
			gui.mainFrame.prePopup()
			d = SettingsTreeDialog(None)
			if d is not None:
				d.Show()
			gui.mainFrame.postPopup()
		wx.CallAfter(run)
	# Translators: the description for the settings tree script.
	script_showSettingsTree.__doc__ = _("Presents a tree of all settings sections, which you can expand to modify all NVDA options")

	__gestures = {
		"kb:NVDA+O": "showSettingsTree",
	}
