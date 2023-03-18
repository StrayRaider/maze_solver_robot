import random
from mz_lib import node

class Robot():
    def __init__(self,parent):
        self.active_depth = 0
        self.parent = parent
        self.founded = False
        self.x = self.parent.start_point[0]
        self.y = self.parent.start_point[1]
        self.grid = self.parent.grid
        self.grid.nodes[(self.x,self.y)].is_moved = True
        self.grid.nodes[(self.x,self.y)].is_saw = True
        self.grid.nodes[(self.x,self.y)].is_used = True
        self.grid.nodes[(self.x,self.y)].real_depth = 0
        self.founded_depth = 0
        self.see_nodes(self.x,self.y)
        self.move_c = 0
        self.parent_back_c = 0

    def see_nodes(self,x,y):
        self.grid.nodes[(x,y)].is_saw = True
        see_list = self.around(x,y)
        for i in see_list:
            i.is_saw = True
        self.set_depth()

    def set_depth(self):
        see_list = self.parent.grid.nodes.values()
        for i in see_list:
            if i.type == 0 and i.is_saw:
                nbh = self.around(i.x,i.y)
                nums = []
                for x in nbh:
                    if x.real_depth != -1:
                        nums.append(x.real_depth)
                smallest_depth = self.smallest(nums)
                if i.real_depth > smallest_depth +1 or i.real_depth == -1:
                    i.real_depth = smallest_depth +1
                    self.set_depth()

    def smallest(self,num_list):
        new_list = []
        for i in num_list:
            if i == -1:
                pass
            else:
                new_list.append(i)
        if len(new_list) == 0:
            return 0
        min_d = new_list[0]
        new_list.sort()
        return new_list[0]

    def around(self,x,y):
        around_l = []
        if x+1 < len(self.grid.maze):
            around_l.append(self.grid.nodes[(x+1,y)])
        if x-1 >= 0:
            around_l.append(self.grid.nodes[(x-1,y)])
        if y+1 < len(self.grid.maze[0]):
            around_l.append(self.grid.nodes[(x,y+1)])
        if y-1 >= 0:
            around_l.append(self.grid.nodes[(x,y-1)])
        return around_l

    def is_able_to_move(self,x,y):
        if self.grid.maze[x][y] != 0:
            return 0
        if self.grid.nodes[(x,y)].is_moved:
            return 0
        return 1

    def move(self):
        self.move_c += 1
        x = self.x
        y = self.y
        # kırmızı yakındaysa direkt ulaş
        if self.parent.is_stop_near(x,y):
            self.move_f(*self.parent.stop_point)
        else:
            rd = random.randint(0,3)
            if rd == 0:
                x+=1
            elif rd == 1:
                x-=1
            elif rd == 2:
                y+=1
            elif rd == 3:
                y-=1
            if self.is_able_to_move(x,y):
                self.move_f(x,y)
            else:
                x = self.x
                y = self.y
                if self.is_able_to_move(x+1,y):
                    self.move_f(x+1,y)
                elif self.is_able_to_move(x-1,y):
                    self.move_f(x-1,y)
                elif self.is_able_to_move(x,y+1):
                    self.move_f(x,y+1)
                elif self.is_able_to_move(x,y-1):
                    self.move_f(x,y-1)
                else:
                    #parenta dönme kodu
                    self.parent_back_c += 1
                    #üzerinde olunan node un girişini kaldır
                    self.grid.nodes[(self.x,self.y)].in_way = None
                    self.active_depth -= 1
                    self.grid.nodes[(self.x,self.y)].is_used = False
                    x = self.grid.nodes[(self.x,self.y)].parent.x
                    y = self.grid.nodes[(self.x,self.y)].parent.y
                    self.x = x
                    self.y = y
                    #parent(geri dönülen) node un çıkışını kaldır
                    self.grid.nodes[(self.x,self.y)].out_way = None
                    self.grid.nodes[(self.x,self.y)].childs = []

    def move_f(self,x,y):
        self.grid.nodes[(x,y)].is_moved = True
        self.grid.nodes[(x,y)].is_used = True
        self.grid.nodes[(x,y)].is_saw = True
        self.active_depth += 1
        self.grid.nodes[(x,y)].parent = self.grid.nodes[(self.x,self.y)]
        self.grid.nodes[(self.x,self.y)].add_child(self.grid.nodes[(x,y)])
        self.set_way(self.grid.nodes[(x,y)])
        self.x = x
        self.y = y
        self.see_nodes(self.x,self.y)

    #gidilen node u alır ve parent ve kendisine yol çeker
    def set_way(self,m_node):
        x = m_node.x - m_node.parent.x
        y = m_node.y - m_node.parent.y
        way = None
        if x == 1:
            way = "up"
        elif x == -1:
            way = "down"
        elif y == 1:
            way = "right"
        elif y == -1:
            way = "left"
        m_node.in_way = way
        m_node.parent.out_way = way


    def go_to_small(self,x,y):
        around = self.around(x,y)
        nums = []
        for i in around:
            nums.append(i.real_depth)
        smallest_depth = self.smallest(nums)
        small_node = None
        for i in around:
            if i.real_depth == smallest_depth:
                small_node = i
        return small_node

    def found(self,x,y):
        self.founded_depth = self.grid.nodes[(x,y)].real_depth
        self.grid.nodes[(x,y)].is_short_way = True
        back_node = self.go_to_small(x,y)
        found_way = [back_node]
        found_way.append(self.grid.nodes[(x,y)])
        back_node.is_short_way = True
        found_way.append(back_node)
        while 1:
            if not back_node.real_depth:
                break
            back_node = self.go_to_small(back_node.x,back_node.y)
            found_way.append(back_node)
            back_node.is_short_way = True
        print("bulunan yol uzunluğu : ",len(found_way))

    def update(self):
        if not self.founded:
            self.move()
        self.active_node_depth= self.grid.nodes[(self.x,self.y)].real_depth
        self.founded_depth = self.active_node_depth
        return True