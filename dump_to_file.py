#!/usr/bin/python

# Plugin by Kaarel Moppel <kaarel.moppel@gmail.com>
# See LICENSE of Terminator package.

"""
dump_to_file.py - Terminator Plugin to save text content of individual terminals to ~/.terminator directory.
Does not need annoying explicit starting of logging like the official "logger" plugin, but will also save only
data thats currently in the scrollback buffer.(so better increase the default buffer size - Preferences->Profiles->Scrolling)
"""

import os
import sys
import gtk
import terminatorlib.plugin as plugin
from terminatorlib.translation import _
import datetime

AVAILABLE = ['DumpToFile']

class DumpToFile(plugin.MenuItem):
    capabilities = ['terminal_menu']
    dumpers = None

    def __init__(self):
        plugin.MenuItem.__init__(self)
        if not self.dumpers:
            self.dumpers = {}

    def callback(self, menuitems, menu, terminal):
        """ Add dump-to-file command to the terminal menu """
        vte_terminal = terminal.get_vte()
        if not self.dumpers.has_key(vte_terminal):
            item = gtk.MenuItem(_('Dump terminal to file'))
            item.connect("activate", self.dump_console, terminal)
        menuitems.append(item)
                        
    def dump_console(self, _widget, Terminal):
        """ Handle menu item callback by saving console text to a predefined location and creating the ~/.terminator folder if necessary """
        try:
            log_folder = os.path.expanduser("~") + "/.terminator/"
            if not os.path.exists(log_folder):
                os.mkdir(log_folder)
            log_file = "console_" + datetime.datetime.now().strftime('%Y-%m-%d_%H%M%S')+".log"
            fd = open(log_folder + log_file, 'w+')
            vte_terminal = Terminal.get_vte()
            col, row = vte_terminal.get_cursor_position()
            content = vte_terminal.get_text_range(0, 0, row, col, lambda *a: True)
            fd.write(content.strip() + "\n")
            fd.flush()
        except Exception as e:
            print e
