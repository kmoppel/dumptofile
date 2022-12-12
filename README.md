## A Terminator plugin

A [Terminator](https://gnome-terminator.org/) plugin for 1-click dumping of the console contents to a text file (`~/.terminator/$datetime.log`).

One needs to copy the plugin to `/usr/share/terminator/terminatorlib/plugins/` or `~/.config/terminator/plugins/` and enable
it under _Preferences_ to make the context-menu (named _DumpToFile_) appear. Dump files are stored under `~/.terminator`,
the directory will be created automatically if not existsing.

For old Gtk2 versions of Terminator (< v1.90) check out a pre-2022 version.

## Usage screenshot

![Usage screenshot](https://raw.githubusercontent.com/kmoppel/dumptofile/master/usage_screenshot.png)
