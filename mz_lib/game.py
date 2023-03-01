import gi, random

path = "./mz_lib/map.txt"

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GObject
from mz_lib import grid, robot

class Game(Gtk.VBox):
    def __init__(self,parent):
        Gtk.VBox.__init__(self)
        self.parent = parent
        self.label = Gtk.Label("Game")
        self.pack_start(self.label,0,0,5)
        self.drawing_area = Gtk.DrawingArea()
        self.drawing_area.connect("draw", self.draw_all)
        self.pack_start(self.drawing_area,1,1,5)
        self.drawing_area.queue_draw()
        self.box_x = 50
        self.box_y = 50
        self.space_x = 2
        self.space_y = 2
        self.robot = None
        self.started = False

        self.start_but = Gtk.Button()
        self.start_but.set_label("Start")
        self.start_but.connect("clicked",self.start_but_clicked)
        self.pack_start(self.start_but,0,0,5)

    def start_but_clicked(self,widget):
        self.timer = GObject.timeout_add(1000/5, self.update)
        if self.started == True:
            self.started = False
            self.start_but.set_label("Start")
        elif self.started == False:
            self.started = True
            self.start_but.set_label("Stop")
        
    def start(self,problem,size = None):
        print(problem,".problem")
        if problem == 1:
            self.solve_problem_1(path)
        if problem == 2:
            self.solve_problem_2(size)
    
    def solve_problem_1(self,path):
        self.grid = grid.Grid(path)
        self.start_point ,self.stop_point = self.problem_1_start_stop()
        self.robot = robot.Robot(self)
        
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
        
    def draw_all(self,widget,cr):
        #print(self.grid.mazle)
        cr.set_source_rgb(0,1,0)
        y = 0
        for row in self.grid.mazle:
            x = 0
            for col in row:
                if (x,y) not in self.robot.is_see:
                    cr.set_source_rgb(0,0,0)
                elif x == self.robot.active_node.x and y == self.robot.active_node.y:
                    cr.set_source_rgb(0,1,0)
                elif x == self.stop_point[0] and y == self.stop_point[1]:
                    cr.set_source_rgb(1,0,0)
                elif (x,y) in self.robot.used_paths(self.robot.root_node):
                    cr.set_source_rgb(0,0,1)
                elif self.grid.mazle[x][y] == 0:
                    cr.set_source_rgb(1,1,1)
                else:
                    cr.set_source_rgb(0.5,0.5,0.5)
                cr.rectangle((self.box_y+self.space_y)*y,(self.box_x+self.space_x)*x,self.box_x,self.box_y)
                cr.fill()
                x+=1
            y+=1
        cr.stroke()
        self.drawing_area.queue_draw()

    def update(self):
        print("here")
        ret = True
        if self.started:
            if self.robot != None:
                ret = self.robot.update()
        else:
            return False
        return ret
