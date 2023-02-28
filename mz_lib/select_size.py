import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

class Select_size(Gtk.VBox):
    def __init__(self,parent):
        Gtk.VBox.__init__(self)
        self.parent = parent
        self.label = Gtk.Label("select_size")
        self.pack_start(self.label,0,0,5)
