import gi, random

path = "./mz_lib/map.txt"

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GObject, GdkPixbuf, Gdk
from mz_lib import grid, robot
import time

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
        self.con_x = 6
        self.con_y = 25
        self.space_x = 2
        self.space_y = 2
        self.robot = None
        self.started = False
        self.fastness = 1000

        self.start_but = Gtk.Button()
        self.start_but.set_label("Start")
        self.start_but.connect("clicked",self.start_but_clicked)

        self.faster = Gtk.Button()
        self.faster.set_label("Faster")
        self.faster.connect("clicked",self.set_faster)
        self.speed_changed = False

        self.pack_start(self.start_but,0,0,5)
        self.pack_start(self.faster,0,0,5)
        self.duvar = GdkPixbuf.Pixbuf.new_from_file_at_scale("./assets/duvar.png", self.box_x, self.box_y, True)
        self.zemin_w = GdkPixbuf.Pixbuf.new_from_file_at_scale("./assets/zemin.png", self.box_x, self.box_y, True)
        self.zemin_g = GdkPixbuf.Pixbuf.new_from_file_at_scale("./assets/zemin_1.png", self.box_x, self.box_y, True)
        self.zemin_b = GdkPixbuf.Pixbuf.new_from_file_at_scale("./assets/zemin_2.png", self.box_x, self.box_y, True)
        self.zemin_y = GdkPixbuf.Pixbuf.new_from_file_at_scale("./assets/zemin_3.png", self.box_x, self.box_y, True)
        self.connect = GdkPixbuf.Pixbuf.new_from_file_at_scale("./assets/connect.png", self.con_x, self.con_y, True)
        self.connect_r = GdkPixbuf.Pixbuf.new_from_file_at_scale("./assets/connect_r.png", self.con_y, self.con_x, True)
        self.connect_r_2 = GdkPixbuf.Pixbuf.new_from_file_at_scale("./assets/connect_r_2.png", self.con_y, self.con_x, True)
        self.robot_p = GdkPixbuf.Pixbuf.new_from_file_at_scale("./assets/robot.png", self.box_x, self.box_y, True)
        self.bulut_w = GdkPixbuf.Pixbuf.new_from_file_at_scale("./assets/bulut_1.png", self.box_x, self.box_y, True)
        self.bulut_d = GdkPixbuf.Pixbuf.new_from_file_at_scale("./assets/bulut_2.png", self.box_x, self.box_y, True)
        self.bulut_n = GdkPixbuf.Pixbuf.new_from_file_at_scale("./assets/bulut_3.png", self.box_x, self.box_y, True)
        self.cizgi_d = GdkPixbuf.Pixbuf.new_from_file_at_scale("./assets/cizgi_d.png", self.con_x, self.con_y, True)
        self.cizgi_y = GdkPixbuf.Pixbuf.new_from_file_at_scale("./assets/cizgi_y.png", self.con_y, self.con_x, True)
        self.start_img = GdkPixbuf.Pixbuf.new_from_file_at_scale("./assets/bb.png", self.box_x, self.box_y, True)

    def set_faster(self,widget):
        self.fastness /= 2
        self.speed_changed = True
        self.timer = GObject.timeout_add(self.fastness, self.update)


    def start_but_clicked(self,widget):
        self.timer = GObject.timeout_add(self.fastness, self.update)
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
        for i in self.grid.nodes.keys():
            m_node = self.grid.nodes[i]
            x = m_node.x
            y = m_node.y
            # kare çizimi
            #if not m_node.is_saw:
            #    Gdk.cairo_set_source_pixbuf(cr, self.bulut_n, (self.box_y+self.space_y)*y,(self.box_x+self.space_x)*x)
            if m_node.is_short_way:
                cr.set_source_rgb(0.9,0.3,0.3)
            elif x == self.stop_point[0] and y == self.stop_point[1]:
                Gdk.cairo_set_source_pixbuf(cr, self.zemin_g, (self.box_y+self.space_y)*y,(self.box_x+self.space_x)*x)
            elif x == self.start_point[0] and y == self.start_point[1]:
                Gdk.cairo_set_source_pixbuf(cr, self.start_img, (self.box_y+self.space_y)*y,(self.box_x+self.space_x)*x)
            elif m_node.is_used:
                Gdk.cairo_set_source_pixbuf(cr, self.zemin_b, (self.box_y+self.space_y)*y,(self.box_x+self.space_x)*x)
            elif m_node.is_moved:
                Gdk.cairo_set_source_pixbuf(cr, self.zemin_y, (self.box_y+self.space_y)*y,(self.box_x+self.space_x)*x)
            elif self.grid.mazle[x][y] == 0:
                Gdk.cairo_set_source_pixbuf(cr, self.zemin_w, (self.box_y+self.space_y)*y,(self.box_x+self.space_x)*x)
            else:
                Gdk.cairo_set_source_pixbuf(cr, self.duvar, (self.box_y+self.space_y)*y,(self.box_x+self.space_x)*x)
            cr.rectangle((self.box_y+self.space_y)*y,(self.box_x+self.space_x)*x,self.box_x,self.box_y)
            cr.fill()
            if not m_node.is_saw:
                Gdk.cairo_set_source_pixbuf(cr, self.bulut_n, (self.box_y+self.space_y)*y,(self.box_x+self.space_x)*x)
                cr.paint()
            if self.robot.x == x and self.robot.y == y:
                Gdk.cairo_set_source_pixbuf(cr, self.robot_p, (self.box_y+self.space_y)*y,(self.box_x+self.space_x)*x)
                cr.paint()
            #yol çizimi:
            if m_node.in_way != None:
                if m_node.in_way == "down":
                    Gdk.cairo_set_source_pixbuf(cr, self.cizgi_d, ((self.box_y+self.space_y)*y)+self.box_y/2,((self.box_x+self.space_x)*x)+self.box_x/2)
                elif m_node.in_way == "up":
                    Gdk.cairo_set_source_pixbuf(cr, self.cizgi_d, ((self.box_y+self.space_y)*y)+(self.box_y-self.con_y),(self.box_x+self.space_x)*x)
                elif m_node.in_way == "left":
                    Gdk.cairo_set_source_pixbuf(cr, self.cizgi_y, ((self.box_y+self.space_y)*y)+(self.box_y-self.con_x)/2,((self.box_x+self.space_x)*x)+(self.box_x-self.con_x)/2)
                elif m_node.in_way == "right":
                    Gdk.cairo_set_source_pixbuf(cr, self.cizgi_y, (self.box_y+self.space_y)*y,((self.box_x+self.space_x)*x)+(self.box_x-self.con_x)/2)
                cr.paint()
            if m_node.out_way != None:
                if m_node.out_way == "up":
                    Gdk.cairo_set_source_pixbuf(cr, self.cizgi_d, ((self.box_y+self.space_y)*y)+self.box_y/2,((self.box_x+self.space_x)*x)+self.box_x/2)
                elif m_node.out_way == "down":
                    Gdk.cairo_set_source_pixbuf(cr, self.cizgi_d, ((self.box_y+self.space_y)*y)+(self.box_y-self.con_y),(self.box_x+self.space_x)*x)
                elif m_node.out_way == "right":
                    Gdk.cairo_set_source_pixbuf(cr, self.cizgi_y, ((self.box_y+self.space_y)*y)+(self.box_y-self.con_x)/2,((self.box_x+self.space_x)*x)+(self.box_x-self.con_x)/2)
                elif m_node.out_way == "left":
                    Gdk.cairo_set_source_pixbuf(cr, self.cizgi_y, (self.box_y+self.space_y)*y,((self.box_x+self.space_x)*x)+(self.box_x-self.con_x)/2)
                cr.paint()
            #self.view_depth(cr,m_node)
        self.drawing_area.queue_draw()

    def view_depth(self,cr,m_node):
            x = m_node.x
            y = m_node.y
            cr.set_source_rgb(0.8,0.8,0.8)
            cr.move_to(((self.box_y+self.space_y)*y)+self.box_y/2,((self.box_x+self.space_x)*x)+self.box_x/2)
            cr.text_path(str(m_node.real_depth))
            cr.stroke()

    def update(self):
        if self.speed_changed == True:
            self.speed_changed = False
            return False
        ret = True
        if self.started:
            if self.robot != None:
                ret = self.robot.update()
        else:
            return False
        return ret