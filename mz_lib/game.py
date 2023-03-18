import gi, random, datetime

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GObject, GdkPixbuf, Gdk
from mz_lib import grid, robot

class Game(Gtk.HBox):
    def __init__(self,parent):
        Gtk.VBox.__init__(self)
        self.parent = parent
        self.label = Gtk.Label("Game")
        #self.pack_start(self.label,0,0,5)
        self.drawing_area = Gtk.DrawingArea()
        self.drawing_area.connect("draw", self.draw_all)
        self.drawing_area.set_size_request(1000,1000)
        self.pack_start(self.drawing_area,1,1,10)
        self.drawing_area.queue_draw()
        self.robot = None
        self.started = False
        self.fastness = 1000

        #self.start_but = Gtk.Button()
        #self.start_but.set_label("Start")
        image = Gtk.Image(stock=Gtk.STOCK_MEDIA_PLAY)
        self.start_but = Gtk.Button(image=image)
        self.start_but.connect("clicked",self.start_but_clicked)

        image = Gtk.Image(stock=Gtk.STOCK_MEDIA_NEXT)
        self.faster = Gtk.Button(image=image)
        self.faster.connect("clicked",self.set_faster)
        self.speed_changed = False

        image = Gtk.Image(stock=Gtk.STOCK_MEDIA_PREVIOUS)
        self.slower = Gtk.Button(image=image)
        self.slower.connect("clicked",self.set_slower)
        self.speed_changed = False

        self.finish = Gtk.Button()
        self.finish.set_label("Finish")
        self.finish.connect("clicked",self.finish_maze)

        self.but_part = Gtk.VBox()
        self.fastness_part = Gtk.HBox()
        self.but_part.pack_start(self.fastness_part,0,0,5)
        self.fastness_part.pack_start(self.slower,0,0,5)
        self.fastness_part.pack_start(self.start_but,0,0,5)
        self.fastness_part.pack_start(self.faster,0,0,5)
        self.but_part.pack_start(self.finish,0,0,5)
        self.pack_start(self.but_part,0,0,5)
        self.max_x_px =950
        self.max_y_px =1700

        self.move_c_label = Gtk.Label("move : 0")
        self.but_part.pack_start(self.move_c_label,0,0,5)

        self.parent_c_label = Gtk.Label("turning back : 0")
        self.but_part.pack_start(self.parent_c_label,0,0,5)

        self.active_depth_label = Gtk.Label("active depth : 0")
        self.but_part.pack_start(self.active_depth_label,0,0,5)

        self.view_depth_but = Gtk.Button(label="Show Depths")
        self.view_depth_but.connect("clicked",self.set_depth_label)
        self.but_part.pack_start(self.view_depth_but,0,0,5)
        self.view_depth_label = False

        self.start_time = datetime.datetime.now()
        self.stop_time = datetime.datetime.now()
        self.time_label = Gtk.Label("Ms : "+str((self.stop_time-self.start_time).seconds))
        self.but_part.pack_start(self.time_label,0,0,5)

        self.turn_back_but = Gtk.Button(label="Turn Back")
        self.but_part.pack_start(self.turn_back_but,0,0,5)

        self.maze_start_x = 0
        self.maze_start_y = 0

    def visible(self):
        self.active_depth_label.set_text("active depth : 0")
        self.parent_c_label.set_text("turning back : 0")
        self.move_c_label.set_text("move : 0")
        self.time_label.set_text("Ms : "+"0")

    def set_depth_label(self,widget):
        if self.view_depth_label == True:
            self.view_depth_label = False
            self.view_depth_but.set_label("Show Depths")
        else:
            self.view_depth_but.set_label("Hide Depths")
            self.view_depth_label = True

    def init_and_scale(self):
        count_x = len(self.grid.maze)
        count_y = len(self.grid.maze[0])
        self.box_x = 50
        self.space_x = 2
        self.box_y = 50
        self.space_y = 2
        scale = 1
        scale_x = 1
        scale_y = 1
        if count_x * (self.box_x + self.space_x) > self.max_x_px:
            scale_x = self.max_x_px/(count_x * (self.box_x + self.space_x))
        if count_y * (self.box_y + self.space_y) > self.max_y_px:
            scale_y = self.max_y_px/(count_y * (self.box_y + self.space_y))
        if scale_x < scale_y:
            scale = scale_x
        elif scale_y < scale_x:
            scale = scale_y
        else:
            scale = scale_y
        self.scale = scale
        self.box_x = 50*scale
        self.box_y = 50*scale
        self.con_x = 6*scale
        self.con_y = 25*scale
        if self.con_x < 1:
            self.con_x = 1
        if self.con_y < 1:
            self.con_y = 1
        self.space_x = 2*scale
        self.space_y = 2*scale

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

        maze_size_x = count_x * (self.box_x + self.space_x)
        maze_size_y = count_y * (self.box_y + self.space_y)
        self.maze_start_x = 0
        self.maze_start_y = 0
        if maze_size_x < self.max_x_px:
            self.maze_start_x = (self.max_x_px - maze_size_x)/2
        if maze_size_y < self.max_y_px:
            self.maze_start_y = (self.max_y_px - maze_size_y)/2

    def set_faster(self,widget,speed_up = 2):
        self.timer = None
        self.fastness /= speed_up
        self.speed_changed = True
        self.timer = GObject.timeout_add(self.fastness, self.update)

    def set_slower(self,widget,speed_up = 2):
        self.timer = None
        self.fastness *= speed_up
        self.speed_changed = True
        self.timer = GObject.timeout_add(self.fastness, self.update)

    def finish_maze(self,widget):
        self.start_but_clicked(None)
        self.set_faster(None,10000)
        self.start_but_clicked(None)

    def start_but_clicked(self,widget):
        self.timer = GObject.timeout_add(self.fastness, self.update)
        if self.started == True:
            self.started = False
            image = Gtk.Image(stock=Gtk.STOCK_MEDIA_PLAY)
        elif self.started == False:
            image = Gtk.Image(stock=Gtk.STOCK_MEDIA_PAUSE)
            self.started = True
        self.start_but.set_image(image)
        self.start_time = datetime.datetime.now()
        
    def start(self,problem,size_path = None,maze_hardness = None):
        if problem == 1:
            self.solve_problem_1(size_path)
        if problem == 2:
            self.solve_problem_2(size_path,maze_hardness)
    
    def solve_problem_1(self,path):
        self.grid = grid.Grid(1,path)
        self.start_point ,self.stop_point = self.problem_1_start_stop()
        #firstly start stop points generates than 3x3 and 2x2 barrier shape changings mades
        self.grid.change_barrier()
        self.robot = robot.Robot(self)
        self.init_and_scale()
        self.turn_back_but.connect("clicked",self.turn_back_2)
        
    def solve_problem_2(self,size,maze_hardness):
        self.start_point ,self.stop_point = self.problem_2_start_stop(int(size[0]),int(size[1]))
        self.grid = grid.Grid(2,size,self.start_point,self.stop_point,maze_hardness)
        self.robot = robot.Robot(self)
        self.init_and_scale()
        self.turn_back_but.connect("clicked",self.turn_back_1)

    def turn_back_1(self,widget):
        self.visible()
        self.parent.stack.set_visible_child_name("select_size")

    def turn_back_2(self,widget):
        self.visible()
        self.parent.stack.set_visible_child_name("read_url")
 
    def problem_2_start_stop(self,size_x,size_y):
        random_num = random.randint(0,4)
        start_point = -1
        stop_point = -1
        if random_num == 0:
            start_point = (1,1)
            stop_point = (size_x-2,size_y-2)
        elif random_num == 1:
            #sağ üst in
            start_point = (size_x-2,1)
            stop_point = (1,size_y-2)
        elif random_num == 2:
            #sol alt in
            start_point = (1,size_y-2)
            stop_point = (size_x-2,1)
        elif random_num == 3:
            #sağ alt in
            start_point = (size_x-2,size_y-2)
            stop_point = (1,1)
        else:
            start_point = (1,1)
            stop_point = (size_x-2,size_y-2)
        return (start_point, stop_point)

    def problem_1_start_stop(self):
        start_point = self.get_point()
        stop_point = self.get_point()
        #if start and stop is same change the stop point
        dist_x = abs(start_point[0]-stop_point[0])
        dist_y = abs(start_point[1]-stop_point[1])
        while stop_point == start_point and dist_x+dist_y<4:
            stop_point = self.get_point()
        return start_point, stop_point
    
    def get_point(self):
        #random start and stop point generator
        x = random.randint(0,len(self.grid.maze)-1)
        y = random.randint(0,len(self.grid.maze[0])-1)
        if self.grid.maze[x][y] != 0:
            return self.get_point()
        else:
            return (x,y)

    def draw_all(self,widget,cr):
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
                Gdk.cairo_set_source_pixbuf(cr, self.zemin_g, self.maze_start_y+(self.box_y+self.space_y)*y,self.maze_start_x+(self.box_x+self.space_x)*x)
            elif x == self.start_point[0] and y == self.start_point[1]:
                Gdk.cairo_set_source_pixbuf(cr, self.start_img, self.maze_start_y+(self.box_y+self.space_y)*y,self.maze_start_x+(self.box_x+self.space_x)*x)
            elif m_node.is_used:
                Gdk.cairo_set_source_pixbuf(cr, self.zemin_b, self.maze_start_y+(self.box_y+self.space_y)*y,self.maze_start_x+(self.box_x+self.space_x)*x)
            elif m_node.is_moved:
                Gdk.cairo_set_source_pixbuf(cr, self.zemin_y, self.maze_start_y+(self.box_y+self.space_y)*y,self.maze_start_x+(self.box_x+self.space_x)*x)
            elif self.grid.maze[x][y] == 0:
                Gdk.cairo_set_source_pixbuf(cr, self.zemin_w, self.maze_start_y+(self.box_y+self.space_y)*y,self.maze_start_x+(self.box_x+self.space_x)*x)
            else:
                Gdk.cairo_set_source_pixbuf(cr, self.duvar, self.maze_start_y+(self.box_y+self.space_y)*y,self.maze_start_x+(self.box_x+self.space_x)*x)
            cr.rectangle(self.maze_start_y+(self.box_y+self.space_y)*y,self.maze_start_x+(self.box_x+self.space_x)*x,self.box_x,self.box_y)
            cr.fill()
            if not m_node.is_saw:
                Gdk.cairo_set_source_pixbuf(cr, self.bulut_n, self.maze_start_y+(self.box_y+self.space_y)*y,self.maze_start_x+(self.box_x+self.space_x)*x)
                cr.paint()
            if self.robot.x == x and self.robot.y == y:
                Gdk.cairo_set_source_pixbuf(cr, self.robot_p, self.maze_start_y+(self.box_y+self.space_y)*y,self.maze_start_x+(self.box_x+self.space_x)*x)
                cr.paint()
            #yol çizimi:
            if m_node.in_way != None:
                if m_node.in_way == "down":
                    Gdk.cairo_set_source_pixbuf(cr, self.cizgi_d,
                        self.maze_start_y+((self.box_y+self.space_y)*y)+self.box_y/2,self.maze_start_x+((self.box_x+self.space_x)*x)+self.box_x/2)
                elif m_node.in_way == "up":
                    Gdk.cairo_set_source_pixbuf(cr, self.cizgi_d,
                        self.maze_start_y+((self.box_y+self.space_y)*y)+(self.box_y-self.con_y),self.maze_start_x+(self.box_x+self.space_x)*x)
                elif m_node.in_way == "left":
                    Gdk.cairo_set_source_pixbuf(cr, self.cizgi_y,
                        self.maze_start_y+((self.box_y+self.space_y)*y)+(self.box_y-self.con_x)/2,self.maze_start_x+((self.box_x+self.space_x)*x)+(self.box_x-self.con_x)/2)
                elif m_node.in_way == "right":
                    Gdk.cairo_set_source_pixbuf(cr, self.cizgi_y,
                        self.maze_start_y+(self.box_y+self.space_y)*y,self.maze_start_x+((self.box_x+self.space_x)*x)+(self.box_x-self.con_x)/2)
                cr.paint()
            if m_node.out_way != None:
                if m_node.out_way == "up":
                    Gdk.cairo_set_source_pixbuf(cr, self.cizgi_d,
                        self.maze_start_y+((self.box_y+self.space_y)*y)+self.box_y/2,self.maze_start_x+((self.box_x+self.space_x)*x)+self.box_x/2)
                elif m_node.out_way == "down":
                    Gdk.cairo_set_source_pixbuf(cr, self.cizgi_d,
                        self.maze_start_y+((self.box_y+self.space_y)*y)+(self.box_y-self.con_y),self.maze_start_x+(self.box_x+self.space_x)*x)
                elif m_node.out_way == "right":
                    Gdk.cairo_set_source_pixbuf(cr, self.cizgi_y,
                        self.maze_start_y+((self.box_y+self.space_y)*y)+(self.box_y-self.con_x)/2,self.maze_start_x+((self.box_x+self.space_x)*x)+(self.box_x-self.con_x)/2)
                elif m_node.out_way == "left":
                    Gdk.cairo_set_source_pixbuf(cr, self.cizgi_y,
                        self.maze_start_y+(self.box_y+self.space_y)*y,self.maze_start_x+((self.box_x+self.space_x)*x)+(self.box_x-self.con_x)/2)
                cr.paint()
            if m_node.real_depth != -1 and self.view_depth_label:
                self.view_depth(cr,m_node)
        self.drawing_area.queue_draw()

    def view_depth(self,cr,m_node):
            x = m_node.x
            y = m_node.y
            cr.set_source_rgb(0.3,0,0)
            cr.move_to(self.maze_start_y+((self.box_y+self.space_y)*y)+self.box_y/4,self.maze_start_x+((self.box_x+self.space_x)*x)+self.box_x/2)
            cr.set_font_size(18*self.scale)
            cr.show_text(str(m_node.real_depth))

    def update_labels(self):
        self.move_c_label.set_label("move : "+str(self.robot.move_c))
        self.parent_c_label.set_label("turning back : "+str(self.robot.parent_back_c))
        self.active_depth_label.set_label("active depth : "+str(self.robot.active_node_depth))

    def is_stop_near(self,x,y):
        if self.stop_point[0] == x-1 and self.stop_point[1] == y:
            return True
        elif self.stop_point[0] == x+1 and self.stop_point[1] == y:
            return True
        if self.stop_point[0] == x and self.stop_point[1] == y-1:
            return True
        elif self.stop_point[0] == x and self.stop_point[1] == y+1:
            return True
        return False

    def update(self):
        if self.robot.x == self.stop_point[0] and self.robot.y == self.stop_point[1]:
            self.robot.found(self.robot.x,self.robot.y)
            self.robot.founded = True
            self.robot.set_depth()
            self.robot.active_node_depth= self.robot.grid.nodes[(self.robot.x,self.robot.y)].real_depth
            self.robot.founded_depth = self.robot.active_node_depth
            self.update_labels()
            return False
        if self.speed_changed == True:
            self.speed_changed = False
            return False
        ret = True
        if self.started:
            if self.robot != None:
                ret = self.robot.update()
        else:
            return False
        self.update_labels()
        self.stop_time = datetime.datetime.now()
        #milliseconds
        self.time_label.set_text("Ms : "+str((self.stop_time-self.start_time).total_seconds() * 1000))
        return ret