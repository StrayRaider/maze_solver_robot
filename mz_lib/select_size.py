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
        self.label = Gtk.Label("select_size")
        self.vert.pack_start(self.label,1,1,5)
        self.entry_x = Gtk.Entry()
        self.entry_y = Gtk.Entry()
        self.label = Gtk.Label("X")
        self.entry_box.pack_start(self.entry_x,1,1,5)
        self.entry_box.pack_start(self.label,1,1,5)
        self.entry_box.pack_start(self.entry_y,1,1,5)
        self.set_size = Gtk.Button(label="Next")
        self.vert.pack_start(self.set_size,0,0,5)
        self.set_size.connect("clicked",self.get_size)
        self.x = 0
        self.y = 0
        self.hardness_combo = Gtk.ComboBoxText()
        self.hardness_combo.append_text("easy")
        self.hardness_combo.append_text("hard")
        self.vert.pack_start(self.hardness_combo,0,0,5)
        self.maze_hardness = True

        self.turn_back_but = Gtk.Button(label="Turn Back")
        self.vert.pack_start(self.turn_back_but,0,0,5)
        self.turn_back_but.connect("clicked",self.turn_back)

    def get_size(self,widget):
        self.x = self.entry_x.get_text()
        self.y = self.entry_y.get_text()
        if self.hardness_combo.get_active_text() == "easy":
            self.maze_hardness = False
        else:
            self.maze_hardness = True
        self.parent.game.start(2,(self.x,self.y),self.maze_hardness)
        self.parent.stack.set_visible_child_name("game")

    def turn_back(self,widget):
        self.parent.stack.set_visible_child_name("problem_select")