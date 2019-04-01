#!/usr/bin/env python
# coding: utf-8
# ezhuthani_lin.py

###############################################################################################
##      എഴുത്താണി  is a FREE software; you can redistribute it and/or modify                 ##   
##      it under the terms of the GNU General Public License as published by                 ##
##      the Free Software Foundation; either version 3 of the License, or                    ##   
##      (at your option) any later version.                                                  ##          
##                                                                                           ##   
##      This program is distributed in the hope that it will be useful,                      ##
##      but WITHOUT ANY WARRANTY; without even the implied warranty of                       ##
##      MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.                                 ##
##      See the GNU General Public License for more details.                                 ##
##                                                                                           ## 
##      You should have received a copy of the GNU General Public License                    ##
##      along with എഴുത്താണി . If not, see <http://www.gnu.org/licenses/>.                   ##
###############################################################################################

import wx
import os
import engine

window_title = 'എഴുത്താണി'

stockUndo = ['']
stockRedo = []
depth = 10			## Default Undo-Redo Depth

class Beditor(wx.Frame):
	def __init__(self, parent, id, title):
		wx.Frame.__init__(self, parent, id, title, size=(800,600))
		
		self.SetIcon(wx.Icon('/usr/share/ezhuthani/icons/icon.png', wx.BITMAP_TYPE_PNG))

		## variables
		self.modify = False
		self.last_name_saved = ''
		self.replace = False
		self.word = ''

		## setting up menubar
		menubar = wx.MenuBar()

		file = wx.Menu()
		#new = wx.MenuItem(file, 101, '&New\tCtrl+N', 'Creates a new document')
		new = wx.MenuItem(file, 101, '&New/പുതിയത്\tCtrl+N', 'Creates a new document/ പുതിയ ഡോക്യുമെൻറ് ഉണ്ടാക്കുന്നു')
		new.SetBitmap(wx.Bitmap('/usr/share/ezhuthani/icons/document_new.png'))
		file.AppendItem(new)

		open = wx.MenuItem(file, 102, '&Open/തുറക്കുക\tCtrl+O', 'Open an existing file')
		open.SetBitmap(wx.Bitmap('/usr/share/ezhuthani/icons/document_open.png'))
		file.AppendItem(open)
		file.AppendSeparator()

		save = wx.MenuItem(file, 103, '&Save/സംഭരിക്കുക\tCtrl+S', 'Save the file')
		save.SetBitmap(wx.Bitmap('/usr/share/ezhuthani/icons/document_save.png'))
		file.AppendItem(save)

		saveas = wx.MenuItem(file, 104, 'Save &As.../വേറേതായി സംഭരിക്കുക...\tShift+Ctrl+S', 'Save the file with a different name')
		saveas.SetBitmap(wx.Bitmap('/usr/share/ezhuthani/icons/document_saveas.png'))
		file.AppendItem(saveas)
		file.AppendSeparator()

		quit = wx.MenuItem(file, 105, '&Quit/പുറത്തു പോകുക\tCtrl+Q', 'Quit the Application')
		quit.SetBitmap(wx.Bitmap('/usr/share/ezhuthani/icons/close.png'))
		file.AppendItem(quit)

		edit = wx.Menu()
		cut = wx.MenuItem(edit, 106, '&Cut/മുറിയ്ക്കുക\tCtrl+X', 'Cut the Selection')
		cut.SetBitmap(wx.Bitmap('/usr/share/ezhuthani/icons/edit_cut.png'))
		edit.AppendItem(cut)

		copy = wx.MenuItem(edit, 107, '&Copy/പകർത്തുക\tCtrl+C', 'Copy the Selection')
		copy.SetBitmap(wx.Bitmap('/usr/share/ezhuthani/icons/edit_copy.png'))
		edit.AppendItem(copy)

		paste = wx.MenuItem(edit, 108, '&Paste/ഒട്ടിക്കുക\tCtrl+V', 'Paste text from clipboard')
		paste.SetBitmap(wx.Bitmap('/usr/share/ezhuthani/icons/edit_paste.png'))
		edit.AppendItem(paste)

		delete = wx.MenuItem(edit, 109, '&Delete/കളയുക', 'Delete the selected text')
		delete.SetBitmap(wx.Bitmap('/usr/share/ezhuthani/icons/edit_delete.png',))

		edit.AppendItem(delete)
		edit.AppendSeparator()
		
		undo = wx.MenuItem(edit, 113, '&Undo/പിൻവലിക്കുക\tCtrl+Z','Undo last change')
		undo.SetBitmap(wx.Bitmap('/usr/share/ezhuthani/icons/arrow_undo.png'))
		redo = wx.MenuItem(edit, 114, '&Redo/ആവർത്തിക്കുക\tCtrl+Y', 'Redo last Undo')
		redo.SetBitmap(wx.Bitmap('/usr/share/ezhuthani/icons/arrow_redo.png'))

		edit.AppendItem(undo)
		edit.AppendItem(redo)
		
		edit.AppendSeparator()
		
		edit.Append(110, 'Select &All /എല്ലാം തിരഞ്ഞെടുക്കുക\tCtrl+A', 'Select the entire text')

		view = wx.Menu()
		view.Append(111, 'Toggle &Statusbar/സ്ഥിതി വിവര രേഖ മാറ്റുക', 'Hide/Show StatusBar')
			
		view.AppendSeparator()
		
		fontsel = wx.MenuItem(view, 501, 'Select &Font/ലിപി തിരഞ്ഞെടുക്കുക', 'Select Font to use in the current document')
		fontsel.SetBitmap(wx.Bitmap('/usr/share/ezhuthani/icons/font.png'))
		view.AppendItem(fontsel)

		view.AppendSeparator()
		
		self.convert = view.Append(503, '&Halt Conversion/ലിപ്യന്തരണം നിർത്തുക\tF11', 'Stops the conversion to Malayalam for the current word(s)', kind = wx.ITEM_CHECK)      

		help = wx.Menu()
		about = wx.MenuItem(help, 112, '&About/സംബന്ധിച്ച്‌', 'About ezhuthani/എഴുത്താണിയെക്കുറിച്ച്')
		about.SetBitmap(wx.Bitmap('/usr/share/ezhuthani/icons/about.png'))
		help.AppendItem(about)
		
		layout_help = wx.MenuItem(help, 502, '&Layout Help/ലിപി രൂപരേഖ സഹായം\tF1', 'Get Help on Key Layout')
		layout_help.SetBitmap(wx.Bitmap('/usr/share/ezhuthani/icons/help.png'))
		help.AppendItem(layout_help)		


		menubar.Append(file, '&File/രേഖ')
		menubar.Append(edit, '&Edit/മാറ്റം വരുത്തുക')
		menubar.Append(view, '&Preferences/പ്രഥമഗണന')
		menubar.Append(help, '&Help/സഹായം')
		self.SetMenuBar(menubar)

		self.Bind(wx.EVT_MENU, self.NewApplication, id=101)
		self.Bind(wx.EVT_MENU, self.OnOpenFile, id=102)
		self.Bind(wx.EVT_MENU, self.OnSaveFile, id=103)
		self.Bind(wx.EVT_MENU, self.OnSaveAsFile, id=104)
		self.Bind(wx.EVT_MENU, self.QuitApplication, id=105)
		self.Bind(wx.EVT_MENU, self.OnCut, id=106)
		self.Bind(wx.EVT_MENU, self.OnCopy, id=107)
		self.Bind(wx.EVT_MENU, self.OnPaste, id=108)
		self.Bind(wx.EVT_MENU, self.OnDelete, id=109)
		self.Bind(wx.EVT_MENU, self.doUndo, id=113)
		self.Bind(wx.EVT_MENU, self.doRedo, id=114)
		self.Bind(wx.EVT_MENU, self.OnSelectAll, id=110)
		self.Bind(wx.EVT_MENU, self.ToggleStatusBar, id=111)
		self.Bind(wx.EVT_MENU, self.OnAbout, id=112)
		self.Bind(wx.EVT_MENU, self.FontSel, id=501)
		self.Bind(wx.EVT_MENU, self.LayoutHelp, id=502)
		self.Bind(wx.EVT_MENU, self.ToggleConvInToolbar, id=503)
				
		
		## setting up toolbar
		self.toolbar = self.CreateToolBar( wx.TB_HORIZONTAL | wx.NO_BORDER | wx.TB_FLAT | wx.TB_TEXT )
		self.toolbar.AddSimpleTool(801, wx.Bitmap('/usr/share/ezhuthani/icons/document_new.png'), 'New/പുതിയത്', '')
		self.toolbar.AddSimpleTool(802, wx.Bitmap('/usr/share/ezhuthani/icons/document_open.png'), 'Open/തുറക്കുക', '')
		self.toolbar.AddSimpleTool(803, wx.Bitmap('/usr/share/ezhuthani/icons/document_save.png'), 'Save/സംഭരിക്കുക', '')
		self.toolbar.AddSeparator()
		
		self.toolbar.AddSimpleTool(804, wx.Bitmap('/usr/share/ezhuthani/icons/edit_cut.png'), 'Cut/മുറിയ്ക്കുക', '')
		self.toolbar.AddSimpleTool(805, wx.Bitmap('/usr/share/ezhuthani/icons/edit_copy.png'), 'Copy/പകർത്തുക', '')
		self.toolbar.AddSimpleTool(806, wx.Bitmap('/usr/share/ezhuthani/icons/edit_paste.png'), 'Paste/ഒട്ടിക്കുക', '')
		self.toolbar.AddSeparator()
		
		self.toolbar.AddSimpleTool(808, wx.Bitmap('/usr/share/ezhuthani/icons/undo_red.png'), 'Undo/പിൻവലിക്കുക (CTRL+Z)', '')
		self.toolbar.AddSimpleTool(809, wx.Bitmap('/usr/share/ezhuthani/icons/redo_red.png'), 'Redo/ആവർത്തിക്കുക (CTRL+Y)', '')
		self.toolbar.AddSeparator()

		self.toolbar.AddSimpleTool(501, wx.Bitmap('/usr/share/ezhuthani/icons/font.png'), 'Select Font/ലിപി തിരഞ്ഞെടുക്കുക', '')
		self.toolbar.AddSimpleTool(502, wx.Bitmap('/usr/share/ezhuthani/icons/help.png'), 'Layout Help/ലിപി രൂപരേഖ സഹായം', '')
		
		self.toolbar.AddSeparator()
		
		self.toolbar.AddCheckTool(504, wx.Bitmap('/usr/share/ezhuthani/icons/cancel.png'),shortHelp='Halt Conversion/ലിപ്യന്തരണം നിർത്തുക (F11)',longHelp='If active, stops the conversion to Malayalam for current word(s)')
		
		self.toolbar.AddSeparator()
		
		self.toolbar.AddSimpleTool(810, wx.Bitmap('/usr/share/ezhuthani/icons/edit_alignment_left.png'), 'Align Left/ഇടത്തേയ്ക്കാക്കുക')
		self.toolbar.AddSimpleTool(811, wx.Bitmap('/usr/share/ezhuthani/icons/edit_alignment_center.png'), 'Align Center/നടുവിലേയ്ക്കാക്കുക')
		self.toolbar.AddSimpleTool(812, wx.Bitmap('/usr/share/ezhuthani/icons/edit_alignment_right.png'), 'Align Right/വലത്തേയ്ക്കാക്കുക')
		self.toolbar.AddSeparator()		

		self.toolbar.AddSimpleTool(813, wx.Bitmap('/usr/share/ezhuthani/icons/edit_bold.png'), 'Bold/കടുപ്പത്തിലാക്കുക')
		self.toolbar.AddSimpleTool(814, wx.Bitmap('/usr/share/ezhuthani/icons/edit_italic.png'), 'Italics/ചരിച്ചെഴുതുക')
		self.toolbar.AddSimpleTool(815, wx.Bitmap('/usr/share/ezhuthani/icons/edit_underline.png'), 'Underline/അടിവരയിടുക')
		self.toolbar.AddSeparator()		

		self.toolbar.AddSimpleTool(807, wx.Bitmap('/usr/share/ezhuthani/icons/close.png'), 'Exit/പുറത്തു പോകുക', '')
		
		self.toolbar.Realize()
		
		self.toolbar.EnableTool( 808, False)
		self.toolbar.EnableTool( 809, False)
		
		self.Bind(wx.EVT_TOOL, self.NewApplication, id=801)
		self.Bind(wx.EVT_TOOL, self.OnOpenFile, id=802)
		self.Bind(wx.EVT_TOOL, self.OnSaveFile, id=803)
		self.Bind(wx.EVT_TOOL, self.OnCut, id=804)
		self.Bind(wx.EVT_TOOL, self.OnCopy, id=805)
		self.Bind(wx.EVT_TOOL, self.OnPaste, id=806)
		self.Bind(wx.EVT_TOOL, self.QuitApplication, id=807)
		self.Bind(wx.EVT_TOOL, self.ToggleConvInMenu, id=504)
		
		####
		
		self.Bind(wx.EVT_TOOL, self.OnTextLeft, id=810)
		self.Bind(wx.EVT_TOOL, self.OnTextCenter, id=811)
		self.Bind(wx.EVT_TOOL, self.OnTextRight, id=812)			
			
		####
		
		
		## setting up the text ctrl
		self.text = wx.TextCtrl(self, 1000, '', size=(-1, -1), style=wx.TE_MULTILINE | wx.TE_PROCESS_ENTER)
		self.text.SetFocus()
		self.text.SetFont(wx.Font(14, wx.DEFAULT, wx.NORMAL, wx.NORMAL, 0, ""))
		self.text.Bind(wx.EVT_TEXT, self.OnTextChanged, id=1000)
		self.text.Bind(wx.EVT_KEY_DOWN, self.OnKeyDown)
		self.text.Bind(wx.EVT_CHAR, self.conv)
		self.text.Bind(wx.EVT_CHAR, self.PreviewConv)
		
		self.Bind(wx.EVT_TOOL, self.doUndo, id = 808)
		self.Bind(wx.EVT_TOOL, self.doRedo, id = 809)
		self.text.Bind(wx.EVT_CHAR, self.populateStore)
		

		self.Bind(wx.EVT_CLOSE, self.QuitApplication)

		self.StatusBar()

		self.Centre()
		self.Show(True)

	## Class Methods
	def NewApplication(self, event):
		editor = Beditor(None, -1, window_title + '[Untitled/പേരു നൽകിയിട്ടില്ല]'  )
		editor.Centre()
		editor.Show()

	def OnOpenFile(self, event):
		file_name = os.path.basename(self.last_name_saved)
		if self.modify:
			dlg = wx.MessageDialog(self, 'Save changes?/മാറ്റങ്ങൾ സംഭരിക്കേണ്ടതുണ്ടോ?', '', wx.YES_NO | wx.YES_DEFAULT | wx.CANCEL |
						wx.ICON_QUESTION)
			val = dlg.ShowModal()
			if val == wx.ID_YES:
				self.OnSaveFile(event)
				self.DoOpenFile()
			elif val == wx.ID_CANCEL:
				dlg.Destroy()
			else:
				self.DoOpenFile()
		else:
			self.DoOpenFile()

	def DoOpenFile(self):
		wcd = 'All files (*)|*|Editor files (*.ef)|*.ef|'
		dir = os.getcwd()
		open_dlg = wx.FileDialog(self, message='Choose a file/ഒരു രേഖ തിരഞ്ഞെടുക്കുക', defaultDir=dir, defaultFile='',
						wildcard=wcd, style=wx.OPEN|wx.CHANGE_DIR)
		if open_dlg.ShowModal() == wx.ID_OK:
			path = open_dlg.GetPath()

			try:
				file = open(path, 'r')
				text = file.read()
				file.close()
				if self.text.GetLastPosition():
					self.text.Clear()
				self.text.WriteText(text)
				self.last_name_saved = path
				self.statusbar.SetStatusText('', 1)
				self.modify = False
				self.SetTitle(window_title + path)
			
			# except IOError, error:
			except IOError:
				dlg = wx.MessageDialog(self, 'Error opening file/രേഖ തുറക്കാന്‍ കഴിയില്ല\n' + str(error))
				dlg.ShowModal()

			# except UnicodeDecodeError, error:
			except UnicodeDecodeError:
				dlg = wx.MessageDialog(self, 'Error opening file/രേഖ തുറക്കാന്‍ കഴിയില്ല\n' + str(error))
				dlg.ShowModal()

		open_dlg.Destroy()
	def OnSaveFile(self, event):
		if self.last_name_saved:

			try:
				file = open(self.last_name_saved, 'w')
				text = self.text.GetValue()
				file.write(text.encode('utf-8'))
				file.close()
				self.statusbar.SetStatusText(os.path.basename(self.last_name_saved) + ' saved/സംഭരിച്ചു', 0)
				self.SetTitle(os.path.basename(self.last_name_saved))
				self.modify = False
				self.statusbar.SetStatusText('', 1)

			# except IOError, error:
			except IOError:
				dlg = wx.MessageDialog(self, 'Error saving file/രേഖ സംഭരിക്കാൻ കഴിയില്ല\n' + str(error))
				dlg.ShowModal()
		else:
			self.OnSaveAsFile(event)

	def OnSaveAsFile(self, event):
		wcd='All files(*)|*|Editor files (*.ef)|*.ef|'
		dir = os.getcwd()
		save_dlg = wx.FileDialog(self, message='Save file as.../വേറേതായി സംഭരിക്കുക...', defaultDir=dir, defaultFile='',
						wildcard=wcd, style=wx.SAVE | wx.OVERWRITE_PROMPT)
		if save_dlg.ShowModal() == wx.ID_OK:
			path = save_dlg.GetPath()

			try:
				file = open(path, 'w')
				text = self.text.GetValue()
				file.write(text.encode('utf-8'))
				file.close()
				self.last_name_saved = os.path.basename(path)
				self.statusbar.SetStatusText(self.last_name_saved + ' saved/സംഭരിച്ചു', 0)
				self.modify = False
				self.statusbar.SetStatusText('', 1)
				self.SetTitle(window_title + path)
			# except IOError, error:
			except IOError:
				dlg = wx.MessageDialog(self, 'Error saving file/രേഖ സംഭരിക്കാൻ കഴിയില്ല\n' + str(error))
				dlg.ShowModal()
		save_dlg.Destroy()

	def OnCut(self, event):
		self.text.Cut()

	def OnCopy(self, event):
		self.text.Copy()

	def OnPaste(self, event):
		self.text.Paste()

	def QuitApplication(self, event):
		if self.modify:
			dlg = wx.MessageDialog(self, 'Save before Exit?/പുറത്തു പോകുന്നതിനു മുൻപ് രേഖ സംഭരിക്കേണ്ടതുണ്ടോ?', '', wx.YES_NO | wx.YES_DEFAULT |
						wx.CANCEL | wx.ICON_QUESTION)
			val = dlg.ShowModal()
			if val == wx.ID_YES:
				self.OnSaveFile(event)
				if not self.modify:
					wx.Exit()
			elif val == wx.ID_CANCEL:
				dlg.Destroy()
			else:
				self.Destroy()
		else:
			self.Destroy()

	def OnDelete(self, event):
		frm, to = self.text.GetSelection()
		self.text.Remove(frm, to)

	def OnSelectAll(self, event):
		self.text.SelectAll()

	#####
	
	def OnTextLeft(self, event):
		style = self.text.GetWindowStyle()
		self.text.SetWindowStyle(style & ~wx.TE_RIGHT | wx.TE_LEFT) 
			
	def OnTextCenter(self, event):
		style = self.text.GetWindowStyle()
		self.text.SetWindowStyle(style & ~wx.TE_RIGHT | wx.TE_CENTER)		

	def OnTextRight(self, event):
		style = self.text.GetWindowStyle()
		self.text.SetWindowStyle(style & ~wx.TE_LEFT | wx.TE_RIGHT)  
	#####

	def OnTextChanged(self, event):
		self.modify = True
		self.statusbar.SetStatusText(' modified', 1)
		event.Skip()

	def OnKeyDown(self, event):
		keycode = event.GetKeyCode()
		if keycode == wx.WXK_INSERT:
			if not self.replace:
				self.statusbar.SetStatusText('INS', 2)
				self.replace = True
			else:
				self.statusbar.SetStatusText('', 2)
				self.replace = False
		event.Skip()

	def ToggleStatusBar(self, event):
		if self.statusbar.IsShown():
			self.statusbar.Hide()
		else:
			self.statusbar.Show()

	def StatusBar(self):
		self.statusbar = self.CreateStatusBar()
		self.statusbar.SetStatusStyles([wx.SB_VERTICAL])
		self.statusbar.SetFieldsCount(3)
		self.statusbar.SetStatusWidths([-13, -3, -2])
		
	def LayoutHelp(self, event):
		info = wx.AboutDialogInfo()

		info.SetIcon(wx.Icon('/usr/share/ezhuthani/icons/ezhuthani.png', wx.BITMAP_TYPE_PNG))
		info.SetName('Layout')
		wx.AboutBox(info)
		
	def ToggleConvInToolbar(self, event):
		if self.convert.IsChecked():
			toggle = True
		else:
			toggle = False
		
		self.toolbar.ToggleTool(504, toggle)
		
	def ToggleConvInMenu(self, event):
		self.convert.Toggle()


	def OnAbout(self, event):

		description = """എഴുത്താണി""" """\n A Malayalam Phonetic Text Editor for GNU/Linux systems\n"""

		licence = """		
		എഴുത്താണി is a FREE software; you can redistribute it and/or modify it under the 
                terms of the GNU General Public License as published by the Free Software Foundation; 
                either version 3 of the License, or (at your option) any later version.
		
		എഴുത്താണി is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; 
		without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR 
		PURPOSE.  See the GNU General Public License for more details. You should have received 
		a copy of the GNU General Public License along with എഴുത്താണി ; if not, write to the Free 
		Software Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  0211"""

		info = wx.AboutDialogInfo()
		
		info.SetIcon(wx.Icon('/usr/share/ezhuthani/icons/logo.png', wx.BITMAP_TYPE_PNG))
		info.SetName('എഴുത്താണി')
		info.SetVersion('0.1')
		info.SetDescription(description)
		info.SetCopyright('LGPL')
		info.SetWebSite('')
		info.SetLicence(licence)
		info.AddDeveloper('Team Ezhuthani')
		info.AddDocWriter('Team Ezhuthani')
		info.AddArtist(':)')
				
		info.SetName('എഴുത്താണി')
		wx.AboutBox(info)
		
		
	
	def FontSel(self, event):
		default_font = wx.Font(14, wx.DEFAULT, wx.NORMAL, wx.NORMAL, 0, "")
		data = wx.FontData()
		
		data.SetAllowSymbols(False)
		data.SetInitialFont(default_font)
		data.SetRange(10, 30)
		dlg = wx.FontDialog(self, data)
		if dlg.ShowModal() == wx.ID_OK:
			data = dlg.GetFontData()
			font = data.GetChosenFont()
			color = data.GetColour()
			text = 'Face: %s, Size: %d, Color: %s' % (font.GetFaceName(), font.GetPointSize(),  color.Get())
			self.text.SetFont(font)
		dlg.Destroy()
	
	def PreviewConv(self, event):
		keycode = event.GetKeyCode()
		
		
		if not self.convert.IsChecked():
			if 32 < keycode <= 126:
				key = chr(keycode)
				self.word += key
				self.statusbar.SetStatusText(engine.roman2mal(self.word))#.encode('utf-8')),0)
			elif keycode == wx.WXK_SPACE:
				self.statusbar.SetStatusText('',0)
				self.word = ''
			elif keycode == wx.WXK_HOME or keycode == wx.WXK_END:
				self.statusbar.SetStatusText('',0)
				self.word = ''
				
			else:
				event.Skip()
				text = self.text.GetRange(0, self.text.GetInsertionPoint()-1)
				
				sow = text.rfind(' ')	## sow = Start of Word (caret position)
					
				if sow == -1:			## Remove the initial space as you are at the beginning of the document
					sow = 0		
					
				self.word = self.text.GetRange(sow, self.text.GetInsertionPoint()-1)
				self.statusbar.SetStatusText(engine.roman2mal(self.word))#.encode('utf-8')),0)
				

		else:
			self.statusbar.SetStatusText('',0)
			self.word = ''
			
		event.Skip()
		
	def populateStore(self, event):
		keycode = event.GetKeyCode()
		if keycode == wx.WXK_SPACE:
			event.Skip()
			stockUndo.append(self.text.GetValue())
			self.toolbar.EnableTool( 808, True)
			if len(stockUndo) > depth:
				del stockUndo[0]
					
		event.Skip()
			
	def doUndo(self, event):
		stockRedo.append(self.text.GetValue())
		if len(stockUndo) == 1:
			self.toolbar.EnableTool( 808, False)
		a = stockUndo.pop()
		self.text.Clear()
		self.text.WriteText(a)
		self.toolbar.EnableTool(809, True)
		
	def doRedo(self, event):
		
		stockUndo.append(self.text.GetValue())
		if len(stockRedo) == 1:
			self.toolbar.EnableTool( 809, False)
		
		a = stockRedo.pop()
		self.text.Clear()
		self.text.WriteText(a)
		self.toolbar.EnableTool(808, True)
	
	###### Converting to Malayalam using engine  ##########
	def conv(self, event):
		keycode = event.GetKeyCode()
				
		if keycode == wx.WXK_SPACE: 
		#if 0 < keycode <= 256:
			key = chr(keycode)
			self.word += key	
			text = self.text.GetRange(0, self.text.GetInsertionPoint())
			wordlist = text.split(' ')
			cur_word = ' ' + wordlist[-1]		## cur_word = current word
			sow = text.rfind(' ')			## sow = start of word (caret position)
			
			#event.Skip()			

			if sow == -1:				## you are at the start of document, so remove the initial space
				sow = 0
				cur_word = cur_word[1:]
			
			if not self.convert.IsChecked():
				self.text.Replace(sow, self.text.GetInsertionPoint(), engine.roman2mal(cur_word))#.encode('utf-8') ))
	
	
		event.Skip()
		


app = wx.App()
Beditor(None, -1, window_title + '[Untitled] / പേരു നൽകിയിട്ടില്ല')
app.MainLoop()
