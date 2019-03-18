#!/usr/bin/env python
# -*- coding: UTF-8 -*-

#-------------------------------------------------------------------------------
# Name:        maskedit.py
# Purpose:
#
# Author:      Maxwell Morais (max.morais.dmm@gmail.com)
#
# Created:     10/04/2013
# Copyright:   (c) Maxwell Morais 2013
# Licence:     MIT
#-------------------------------------------------------------------------------

import sys
import re
import calendar

if sys.version[0]=='2':
    import Tkinter as tk
    import ttk
    import tkFont
elif sys.version[0]=='3':
    import tkinter as tk
    import tkinter.font as tkFont
    from tkinter import ttk
    basestring = type(u'')
else:
    print("Python version not supported, try 2 or 3 versios")

definitions = {
    '9': '[0-9]',
    'a': '[a-zA-Z]',
    'x': '[a-zA-z0-9]'
}

class MaskedWidget(ttk.Entry):
    def __init__(self, master, format_type, **kw):
        self.fields = {
            'type': format_type,
            'mask': None,
            'monetary': False,
            'dec_places': 2,
            'dec_sep': '.',
            'tho_places': 3,
            'tho_sep': ',',
            'symbol': '',
            'fmt_neg': '-%(symbol)s%(amount)s',
            'fmt_pos': '%(symbol)s%(amount)s',
            'placeholder': '_',
            'textvariable': None,
        }

        if str(format_type).lower() == 'fixed':
            assert 'mask' in kw, 'the fixed mask, is not present'

        self.fields['mask'] = kw.pop('mask', '').lower()
        for k in list(kw.keys()):
            if k in self.fields:
                if k!='textvariable':
                    self.fields[k]=kw.pop(k)
                else:
                    self.fields[k]=kw[k]
        if not 'textvariable' in kw:
            self.fields['textvariable']=tk.StringVar(master)
            kw['textvariable'] = self.fields['textvariable']
        ttk.Entry.__init__(self, master, **kw)

        self.defs = definitions
        self.tests = []
        self.partialPosition = None
        self.firstNonMaskPosition = None
        self.len = len(self.fields['mask'])
        for i,c in enumerate(self.fields['mask'].lower()):
            if c == '?':
                self.len -= 1
                self.partialPosition = i
            atom = self.defs.get(c, None)
            self.tests.append(re.compile('(%s)'%atom) if atom else atom)
            if not atom and self.firstNonMaskPosition==None:
                self.firstNonMaskPosition = len(self.tests)-1

        self.writeBuffer()

        if str(self.cget("state")).upper()!="DISABLED":
            self.bind('<KeyPress>', self._onKeyPress, True)
            self.bind('<KeyRelease>', lambda e: 'break', True)
            self.bind('<FocusIn>', self._onFocusIn, True)

    def clean_numeric(self, string):
        if not isinstance(string, basestring): string = str(string)
        string = string.replace(self.fields['symbol']+' ', '')\
                       .replace(self.fields['tho_sep'], '')\
                       .replace(self.fields['dec_sep'], '.')
        if not '.' in string:
            string = list(string)
            string.insert(-2, '.')
            string = ''.join(string)
        return string.partition('.')

    def fmt_numeric( self, amount):
        temp = '00' if not '.' in str(amount) \
                    else str(amount).split('.')[1]
        l = []
        amount = amount.split('.')[0]
        try:
            minus = float(''.join(self.clean_numeric(amount)))<0
        except ValueError:
            minus = 0
        if len(amount)> self.fields['tho_places']:
            nn = amount[-self.fields['tho_places']:]
            l.append(nn)
            amount = amount[:len(amount)-self.fields['tho_places']]
            while len(amount) > self.fields['tho_places']:
                nn = amount[len(amount)-self.fields['tho_places']:]
                l.insert(0, nn)
                amount = amount[0:len(amount)-self.fields['tho_places']]

        if len(''.join(self.clean_numeric(amount)))>0: l.insert(0, amount)
        amount = self.fields['tho_sep'].join(l)+self.fields['dec_sep']+temp
        if minus:
            amount = self.fields['fmt_neg']%{
                'symbol':self.fields['symbol'],
                'amount': amount
            }
        else:
            amount = self.fields['fmt_pos']%{
                'symbol': (self.fields['symbol']+' ') if self.fields['symbol'] else '',
                'amount': amount
            }
        return amount

    def seekNext(self, pos):
        if 0 <= pos+1<self.len:
            if self.tests[pos+1]:
                return pos+1
            return self.seekNext(pos+1)
        return pos

    def seekPrev(self, pos):
        if 0 <= pos-1 < self.len:
            if self.tests[pos-1]:
                return pos-1
            return self.seekPrev(pos-1)
        return pos

    def shiftL(self, begin, end):
        if begin < 0: return
        for i in range(self.len):
            j = self.seekNext(begin)
            if self.tests[i]:
                if j < self.len and self.tests[i].match(self.buffer[i]):
                    self.buffer[i] = self.buffer[j]
                    self.buffer[j] = self.fields['placeholder']
                else:
                    break

    def shiftR(self, pos, c):
        if pos in range(len(self.len)):
            j = self.seekNext(pos)
            t = self.buffer[pos]
            if not t == c and j < self.len and t == self.fields['placeholder']:
                self.buffer[pos] = c

    def writeBuffer(self):
        self.fields['textvariable'].set(
            ''.join(
                filter(
                    lambda x: x!=None,
                        map(
                            lambda c, self=self:
                                (self.fields['placeholder']
                                if self.defs.get(c, None)
                        else c)
                    if c!='?' else None, self.fields['mask'])
                )
            )
        )
        return self.get()

    def _onFocusIn(self, event):
        if self.len>0 and self.tests[0]:
            self.icursor(0)
        else:
            self.icursor(self.seekNext(0))

    def _onKeyPress(self, event):
        if event.keysym == 'Tab':
            return
        elif event.keysym == 'Escape':
            if self.fields['type'] == 'fixed':
                self.writeBuffer()
            else:
                self.delete(0, len(event.widget.get()))
        widget = event.widget
        val = widget.get()
        idx = widget.index(tk.INSERT)

        if event.keysym == 'Left':
            if 0 <= idx < self.len:
                if idx < self.firstNonMaskPosition:
                    return 'break'
                elif not self.tests[idx]:
                    widget.icursor(self.seekPrev(idx))
        elif event.keysym == 'Right':
            if 0 <= idx < self.len:
                if idx >= self.len:
                    return 'break'
                elif not self.tests[idx]:
                    widget.icursor(self.seekNext(idx))
        elif event.keysym == 'BackSpace' and self.fields['type'] != 'numeric':
            def repl_or_stop(cls, wget, pos):            
                if 0 <= pos <= cls.len:
                    if not cls.tests[pos]:
                        pos = cls.seekPrev(pos)
                    cls._write_char(pos, cls.fields['placeholder'], -1)
                return 'break'
            repl_or_stop(self, widget, idx - 1)
            return 'break'
        else:
            if self.fields['type'] == 'fixed':
                if self._write_char(idx, event.char) == 'break':
                    return 'break'
            elif self.fields['type'] == 'numeric' and event.char.isdigit():
                if val:
                    widget.delete(0, len(val))
                    head, sep, tail = self.clean_numeric(val)
                else:
                    head, sep, tail = '0', '.', '00'

                if not head:
                    head = '0'
                if len(tail) < 2:
                    tail = '0' + tail

                if tail and len(tail + event.char) <= 2 and (int(tail+event.char))<99:
                    tail = tail[1:] + event.char
                else:
                    if not int(head):
                        head = tail[0] if tail else '0'
                    else:
                        head += tail[0]
                    tail = tail[1:] + event.char
                    widget.insert(0, ''.join([head, sep, tail]))
                return 'break'
            elif self.fields['type'] == 'numeric' and event.keysym == 'BackSpace':
                if val:
                    widget.delete(0, len(val))
                    head, sep, tail = self.clean_numeric(val[:-1])
                else:
                    head, sep, tail = '0', '.', '00'
                widget.insert(0, ''.join([head, sep, tail]))
                return 'break'
            else:
                self.bell()
                return 'break'

    def insert(self, index, value):
        if self.fields['type']=='numeric':
            ttk.Entry.insert(self, index, self.fmt_numeric(value))
        else:
            for c in str(value):
                while (not self.tests[index] or not self.tests[index].match(c)):
                    index += 1
                self._write_char(index,c)
                index += 1

    def _write_char(self, idx, char, direction=+1):
        if 0<=idx<self.len and self.tests[idx]:
            if char != self.fields['placeholder'] and not self.tests[idx].match(char):
                self.bell()
                return 'break'
            self.delete(idx)
            ttk.Entry.insert(self, idx, char)
            if direction == +1:
                if idx + 1 < self.len and not self.tests[idx+1]:
                    idx = self.seekNext(idx)
                else:
                    idx += 1
            elif direction == -1 and \
                idx - 1 >= 0 and \
                not self.tests[idx]:
                idx = self.seekPrev(idx)
            self.icursor(idx)
            return 'break'
        else:
            self.bell()
            return 'break'
