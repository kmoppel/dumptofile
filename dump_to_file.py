# Plugin by Kaarel Moppel <kaarel.moppel@gmail.com>
# See LICENSE of Terminator package.

"""
dump_to_file.py - Terminator Plugin to save text content of individual terminals to ~/.terminator directory.
Does not need annoying explicit starting of logging like the official "logger" plugin, but will also save only
data thats currently in the scrollback buffer.(so better increase the default buffer size - Preferences->Profiles->Scrolling)
"""

import os
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Vte
import terminatorlib.plugin as plugin
from terminatorlib.translation import _
import datetime
from terminatorlib.util import dbg

AVAILABLE = ['DumpToFile']


class DumpToFile(plugin.MenuItem):
    capabilities = ['terminal_menu']
    dumpers = None
    vte_minor_version = None

    def __init__(self):
        plugin.MenuItem.__init__(self)
        if not self.dumpers:
            self.dumpers = {}

    def callback(self, menuitems, menu, terminal):
        """ Add dump-to-file command to the terminal menu """
        vte_terminal = terminal.get_vte()
        if vte_terminal not in self.dumpers:
            item = Gtk.MenuItem.new_with_mnemonic(_('D_ump terminal to file'))
            item.connect("activate", self.dump_console, terminal)
            menuitems.append(item)
            self.vte_minor_version = Vte.get_minor_version()
            dbg("Vte.get_minor_version(): %s" % self.vte_minor_version)

    def dump_console(self, _widget, Terminal):
        """ Handle menu item callback by saving console text to a predefined location and creating the ~/.terminator folder if necessary """
        try:
            log_folder = os.path.join(os.path.expanduser("~"), ".terminator")
            if not os.path.exists(log_folder):
                os.mkdir(log_folder)
            log_file = "console_" + datetime.datetime.now().strftime('%Y-%m-%d_%H%M%S') + ".log"
            vte = Terminal.get_vte()
            dbg("Terminal.get_vte(): %s" % vte)
            col, row = vte.get_cursor_position()
            if self.vte_minor_version and self.vte_minor_version < 72:
                content = vte.get_text_range(0, 0, row, col, lambda *a: True)
            else:
                content = vte.get_text_range_format(Vte.Format.TEXT, 0, 0, row, col)
            if content and content[0]:
                fd = open(os.path.join(log_folder, log_file), 'w+')
                fd.write(content[0])
                fd.flush()
        except Exception as e:
            print(e)
