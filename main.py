import random, gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from mz_lib import grid, problems, game, select_size

class MyWindow(Gtk.Window):
    def __init__(self):
        super().__init__(title="Youtube Installation")

        self.stack = Gtk.Stack()
        self.add(self.stack)
        self.stack.set_transition_type(Gtk.StackTransitionType.SLIDE_LEFT_RIGHT)
        self.stack.set_transition_duration(1000)
        self.stack.add_titled(problems.Problems(self),"problem_select","choice_screen")
        self.game = game.Game(self)
        self.stack.add_titled(self.game,"game","choice_screen")
        self.stack.add_titled(select_size.Select_size(self),"select_size","choice_screen")
        self.problem = 0
        
        
        
win = MyWindow()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()
