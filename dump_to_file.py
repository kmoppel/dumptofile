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
        """ Add dump-to-file commands to the terminal menu """
        vte_terminal = terminal.get_vte()
        if vte_terminal not in self.dumpers:
            item = Gtk.MenuItem.new_with_mnemonic(_('D_ump terminal to file'))
            item.connect("activate", self.dump_console, terminal, False)
            menuitems.append(item)
            item = Gtk.MenuItem.new_with_mnemonic(_('Dump terminal to file - _choose location'))
            item.connect("activate", self.dump_console, terminal, True)
            menuitems.append(item)
            self.vte_minor_version = Vte.get_minor_version()
            dbg("Vte.get_minor_version(): %s" % self.vte_minor_version)

    def default_log_folder(self):
        """ Return the default ~/.terminator log folder, creating it if necessary """
        log_folder = os.path.join(os.path.expanduser("~"), ".terminator")
        if not os.path.exists(log_folder):
            os.mkdir(log_folder)
        return log_folder

    def default_log_name(self):
        """ Return a default log file name based on the current timestamp """
        return "console_" + datetime.datetime.now().strftime('%Y-%m-%d_%H%M%S') + ".log"

    def write_content(self, Terminal, path):
        """ Extract the terminal scrollback buffer content and write it to the given path """
        vte = Terminal.get_vte()
        dbg("Terminal.get_vte(): %s" % vte)
        col, row = vte.get_cursor_position()
        if self.vte_minor_version and self.vte_minor_version < 72:
            content = vte.get_text_range(0, 0, row, col, lambda *a: True)
        else:
            content = vte.get_text_range_format(Vte.Format.TEXT, 0, 0, row, col)
        if content and content[0]:
            fd = open(path, 'w+')
            fd.write(content[0])
            fd.flush()

    def dump_console(self, _widget, Terminal, choose_location):
        """ Handle menu item callback: one-click save to ~/.terminator, or via a save dialog when choose_location is set """
        try:
            if choose_location:
                save_dialog = Gtk.FileChooserDialog(title=_("Save log"),
                                               action=Gtk.FileChooserAction.SAVE,
                                               buttons=(_("_Cancel"), Gtk.ResponseType.CANCEL, _("_Save"), Gtk.ResponseType.OK))
                save_dialog.set_transient_for(_widget.get_toplevel())
                save_dialog.set_do_overwrite_confirmation(True)
                save_dialog.set_local_only(True)
                save_dialog.set_current_folder(self.default_log_folder())
                save_dialog.set_current_name(self.default_log_name())
                save_dialog.show_all()
                response = save_dialog.run()
                if response == Gtk.ResponseType.OK:
                    self.write_content(Terminal, save_dialog.get_filename())
                save_dialog.destroy()
            else:
                self.write_content(Terminal, os.path.join(self.default_log_folder(), self.default_log_name()))
        except Exception as e:
            print(e)
