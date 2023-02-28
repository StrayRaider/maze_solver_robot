import gi, random

path = "./mz_lib/map.txt"

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from mz_lib import grid, robot

class Game(Gtk.VBox):
    def __init__(self,parent):
        Gtk.VBox.__init__(self)
        self.parent = parent
        self.label = Gtk.Label("Game")
        self.pack_start(self.label,0,0,5)
        
    def start(self,problem,size = None):
        print(problem,".problem")
        if problem == 1:
            self.solve_problem_1(path)
        if problem == 2:
            self.solve_problem_2(size)
    
    def solve_problem_1(self,path):
        self.grid = grid.Grid(path)
        self.robot = robot.Robot(self)
        self.problem_1_start_stop()
        
    def solve_problem_2(self,size):
        self.grid = grid.Grid(size)
        self.robot = robot.Robot(self)
        
    def problem_1_start_stop(self):
        start_point = self.get_point()
        stop_point = self.get_point()
        #if start and stop is same change the stop point
        while stop_point == start_point:
            stop_point = self.get_point()
        return start_point, stop_point
    
    def get_point(self):
        #random start and stop point generator
        x = random.randint(0,len(self.grid.mazle)-1)
        y = random.randint(0,len(self.grid.mazle[0])-1)
        #print(self.grid.mazle)
        #print(self.grid.mazle[x][y])
        if self.grid.mazle[x][y] != 0:
            return self.get_point()
        else:
            return (x,y)
            
    #yer tutucu komple düzenlenmeli
    def problem_2_start_stop(self):
        start_point = get_point()
        stop_point = get_point()
        return 
