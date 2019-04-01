#/usr/bin/env python
# coding: utf-8
## keymaps.py


###############################################################################################
##					Copyright 2013 IITMK
##
##	This file is part of എഴുത്താണി  : A Malayalam Phonetic Text Editor for GNU/Linux Systems
##
##      എഴുത്താണി  is FREE software; you can redistribute it and/or modify
##      it under the terms of the GNU General Public License as published by
##      the Free Software Foundation; either version 3 of the License, or
##      (at your option) any later version.
##       
##      This program is distributed in the hope that it will be useful,
##      but WITHOUT ANY WARRANTY; without even the implied warranty of
##      MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  
##      See the GNU General Public License for more details.
##       
##      You should have received a copy of the GNU General Public License
##      along with എഴുത്താണി . If not, see <http://www.gnu.org/licenses/>.
###############################################################################################

import wx

''' Keymaps: Lists the keymaps for use with engine.py '''


keymap = {}

#keymap[' '] = u'\u0020';
#keymap['\b'] = u'\u0020';
#keymap[wx.WXK_ESCAPE] = u'<ESCAPE>';
#keymap[wx.WXK_BACK] = u'<BACK>';
#keymap[wx.WXK_RETURN] = u'<RETURN>';

keymap['0'] = '0';
keymap['1'] = '1';
keymap['2'] = '2';
keymap['3'] = '3';
keymap['4'] = '4';
keymap['5'] = '5';
keymap['6'] = '6';
keymap['7'] = '7';
keymap['8'] = '8';
keymap['9'] = '9';

keymap['a'] = u'\u0D05';
keymap['A'] = u'\u0D06';
keymap['i'] = u'\u0D07';
keymap['I'] = u'\u0D08';
keymap['u'] = u'\u0D09';
keymap['U'] = u'\u0D0A';
keymap['x'] = u'\u0D0B'; 
keymap['e'] = u'\u0D0E';
keymap['E'] = u'\u0D0F';
keymap['Y'] = u'\u0D10';
keymap['o'] = u'\u0D12';
keymap['O'] = u'\u0D13';
keymap['Q'] = u'\u0D14';

keymap['acihnam'] = '';
keymap['Acihnam'] = u'\u0D3E';
keymap['icihnam'] = u'\u0D3F';
keymap['Icihnam'] = u'\u0D40';
keymap['ucihnam'] = u'\u0D41';
keymap['Ucihnam'] = u'\u0D42';
keymap['xcihnam'] = u'\u0D43'
keymap['ecihnam'] = u'\u0D46';
keymap['Ecihnam'] = u'\u0D47';
keymap['ocihnam'] = u'\u0D4A';
keymap['Ocihnam'] = u'\u0D4B';
keymap['Ycihnam'] = u'\u0D48';
keymap['Qcihnam'] = u'\u0D57';
keymap['M'] = u'\u0D02';
keymap['H'] = u'\u0D03'; 
#keymap['Xcihnam'] = 'ൃ';
#കഖഗഘങചഛജഝഞടഠഡഢണ
keymap['chandra'] = u'\u0D4D';

keymap['k'] = u'\u0D15';
keymap['kh'] = u'\u0D16';
keymap['g'] = u'\u0D17';
keymap['gh'] = u'\u0D18';
keymap['G'] = u'\u0D19';
keymap['c'] = u'\u0D1A';
keymap['ch'] = u'\u0D1B';
keymap['C'] = u'\u0D1B';
keymap['j'] = u'\u0D1C';
keymap['jh'] = u'\u0D1D';
keymap['J'] = u'\u0D1E';
keymap['T'] = u'\u0D1F';
keymap['Th'] = u'\u0D20';
keymap['D'] = u'\u0D21';
keymap['Dh'] = u'\u0D22';
keymap['N'] = u'\u0D23';  
keymap['t'] = u'\u0D24';     #തഥദധനപഫബഭമയരലവശഷസഹളഴറ
keymap['th'] = u'\u0D25';
keymap['d'] = u'\u0D26';
keymap['dh'] = u'\u0D27';
keymap['n'] = u'\u0D28';
keymap['p'] = u'\u0D2A';
keymap['ph'] = u'\u0D2B';
keymap['b'] = u'\u0D2C';
keymap['bh'] = u'\u0D2D';
keymap['m'] = u'\u0D2E';
keymap['y'] = u'\u0D2F';
keymap['r'] = u'\u0D30';
keymap['l'] = u'\u0D32';
keymap['v'] = u'\u0D35';
keymap['sh'] = u'\u0D37';
keymap['S'] = u'\u0D36';
keymap['s'] = u'\u0D38';
keymap['h'] = u'\u0D39';
keymap['L'] = u'\u0D33';
keymap['z'] = u'\u0D34';
keymap['R'] = u'\u0D31';

keymap['^'] = u'\u0D4D';

keymap['N~'] = u'\u0D7A';    		#ൽൾർൺൻ
keymap['n~'] = u'\u0D7B';
keymap['r~'] = u'\u0D7C';
keymap['l~'] = u'\u0D7D';
keymap['l^~'] = u'\u0D7E';



#keymap['Y']='';
keymap['W'] = ''
keymap['Z'] = ''
keymap['P'] = ''
keymap['F'] = ''
keymap['K'] = ''
keymap['V'] = ''
keymap['B'] = ''
keymap['X']=''
keymap['q']=''


keymap['#'] = '‌'; # zero-width non-joiner ?

