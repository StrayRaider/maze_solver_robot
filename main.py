import random, gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk
from mz_lib import grid, problems, game, select_size, read_url

class MyWindow(Gtk.Window):
    def __init__(self):
        super().__init__(title="Mazle Solver")
        self.stack = Gtk.Stack()
        self.add(self.stack)
        self.stack.set_transition_type(Gtk.StackTransitionType.SLIDE_LEFT_RIGHT)
        self.stack.set_transition_duration(3000)
        self.stack.add_titled(problems.Problems(self),"problem_select","choice_screen")
        self.stack.add_titled(select_size.Select_size(self),"select_size","choice_screen")
        self.stack.add_titled(read_url.Select_size(self),"read_url","choice_screen")
        self.game = game.Game(self)
        self.stack.add_titled(self.game,"game","choice_screen")
        self.problem = 0
        self.max_x = 1900
        self.max_y = 1000
        self.set_size_request(self.max_x,self.max_y)
        log_f = open("log.txt","w")
        log_f.close()

win = MyWindow()

win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()