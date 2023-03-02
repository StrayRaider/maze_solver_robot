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
        self.grid.nodes[(self.x,self.y)].is_used = True
        self.saw_nodes(self.x,self.y)

    def saw_nodes(self,x,y):
        self.grid.nodes[(x,y)].is_saw = True
        self.grid.nodes[(x+1,y)].is_saw = True
        self.grid.nodes[(x-1,y)].is_saw = True
        self.grid.nodes[(x,y+1)].is_saw = True
        self.grid.nodes[(x,y-1)].is_saw = True

    def is_able_to_move(self,x,y):
        if self.grid.mazle[x][y] != 0:
            return 0
        if self.grid.nodes[(x,y)].is_moved:
            return 0
        return 1

    def move(self):
        x = self.x
        y = self.y
        # kırmızı yakındaysa direkt ulaş
        if self.is_stop_near(x,y):
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
                    self.active_depth -= 1
                    print(self.active_depth)
                    self.grid.nodes[(self.x,self.y)].is_used = False
                    x = self.grid.nodes[(self.x,self.y)].parent.x
                    y = self.grid.nodes[(self.x,self.y)].parent.y
                    self.x = x
                    self.y = y
                    self.grid.nodes[(self.x,self.y)].childs = []
                    print("parenta dönüldü")

    def is_stop_near(self,x,y):
        if self.parent.stop_point[0] == x-1 and self.parent.stop_point[1] == y:
            return True
        elif self.parent.stop_point[0] == x+1 and self.parent.stop_point[1] == y:
            return True
        if self.parent.stop_point[0] == x and self.parent.stop_point[1] == y-1:
            return True
        elif self.parent.stop_point[0] == x and self.parent.stop_point[1] == y+1:
            return True
        return False

    def move_f(self,x,y):
        print(self.active_depth)
        self.grid.nodes[(x,y)].is_moved = True
        self.grid.nodes[(x,y)].is_used = True
        self.active_depth += 1
        self.grid.nodes[(x,y)].parent = self.grid.nodes[(self.x,self.y)]
        self.grid.nodes[(self.x,self.y)].add_child(self.grid.nodes[(x,y)])
        self.x = x
        self.y = y
        self.saw_nodes(self.x,self.y)

    def update(self):
        self.move()
        if self.x == self.parent.stop_point[0] and self.y == self.parent.stop_point[1]:
            return False 
        print(self.x,self.y)
        return True