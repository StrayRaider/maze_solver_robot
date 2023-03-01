import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

class Problems(Gtk.VBox):
    def __init__(self,parent):
        Gtk.VBox.__init__(self)
        self.parent = parent
        self.label = Gtk.Label("choice")
        self.pack_start(self.label,0,0,5)
        
        self.problem1 = Gtk.Button()
        self.problem1.set_label("Problem 1")
        self.problem1.connect("clicked",self.problem_1_clicked)
        
        self.problem2 = Gtk.Button()
        self.problem2.set_label("Problem 2")
        self.problem2.connect("clicked",self.problem_2_clicked)
        self.pack_start(self.problem1,0,0,5)
        self.pack_start(self.problem2,0,0,5)
        
    def problem_1_clicked(self,widget):
        self.parent.game.start(1)
        self.parent.stack.set_visible_child_name("file_chooser")
    
    def problem_2_clicked(self,widget):
        self.parent.stack.set_visible_child_name("select_size")
