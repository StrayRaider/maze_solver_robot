import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

class Select_size(Gtk.VBox):
    def __init__(self,parent):
        Gtk.VBox.__init__(self)
        self.parent = parent
        self.vert = Gtk.VBox()
        self.entry_box = Gtk.HBox()
        self.pack_start(self.vert,0,0,5)
        self.vert.pack_start(self.entry_box,0,0,5)
        self.label = Gtk.Label("read url")
        self.vert.pack_start(self.label,1,1,5)
        self.url_entry = Gtk.Entry()
        self.entry_box.pack_start(self.url_entry,1,1,5)
        self.set_size = Gtk.Button(label="Read")
        self.vert.pack_start(self.set_size,0,0,5)
        self.set_size.connect("clicked",self.start)

    def start(self,widget):
        url = self.url_entry.get_text()
        self.parent.game.start(1,url)
        #self.parent.game.start(1,"./mz_lib/maps/url1.txt")
        self.parent.stack.set_visible_child_name("game")