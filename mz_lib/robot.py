import random

class Robot():
    def __init__(self,parent):
        self.root_node = Node(*parent.start_point,None)
        self.active_node = self.root_node
        self.parent = parent
        self.founded = False
        self.used_paths(self.root_node)
        self.is_see = []
        self.is_see.append((self.active_node.x,self.active_node.y))
        self.is_see.append((self.active_node.x+1,self.active_node.y))
        self.is_see.append((self.active_node.x-1,self.active_node.y))
        self.is_see.append((self.active_node.x,self.active_node.y+1))
        self.is_see.append((self.active_node.x,self.active_node.y-1))
        self.moved = []
        self.moved.append((self.active_node.x,self.active_node.y))

    def move(self):
        x = self.active_node.x
        y = self.active_node.y
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
                x = self.active_node.x
                y = self.active_node.y
                if self.is_able_to_move(x+1,y):
                    self.move_f(x+1,y)
                elif self.is_able_to_move(x-1,y):
                    self.move_f(x-1,y)
                elif self.is_able_to_move(x,y+1):
                    self.move_f(x,y+1)
                elif self.is_able_to_move(x,y-1):
                    self.move_f(x,y-1)
                else:
                    self.active_node = self.active_node.parent
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
        if (x,y) not in self.moved:
            self.moved.append((x,y))
        if (x,y) not in self.is_see:
            self.is_see.append((x,y))
        if (x+1,y) not in self.is_see:
            self.is_see.append((x+1,y))
        if (x-1,y) not in self.is_see:
            self.is_see.append((x-1,y))
        if (x,y+1) not in self.is_see:
            self.is_see.append((x,y+1))
        if (x,y-1) not in self.is_see:
            self.is_see.append((x,y-1))
        new_step = Node(x,y,self.active_node)
        new_step.parent = self.active_node
        self.active_node.add_child(new_step)
        self.active_node = new_step

    def is_able_to_see(self):
        is_see = []
        for i in self.used_paths(self.root_node):
            if i not in is_see:
                is_see.append(i)
            elif (i[0]+1,i[1]) not in is_see:
                is_see.append((i[0]+1,i[1]))
            elif (i[0]-1,i[1]) not in is_see:
                is_see.append((i[0]-1,i[1]))
            elif (i[0],i[1]+1) not in is_see:
                is_see.append((i[0],i[1]+1))
            elif (i[0],i[1]-1) not in is_see:
                is_see.append((i[0],i[1]-1))
        return is_see

    def is_able_to_move(self,x,y):
        if self.parent.grid.mazle[x][y] != 0:
            return 0
        if self.is_gone(x,y):
            return 0
        return 1

    def is_gone(self,x,y):
        if (x,y) in self.used_paths(self.root_node):
            return 1
        return 0

    def used_paths(self,up_node,used_list = []):
        for i in up_node.childs:
            used_list.append((i.x,i.y))
            self.used_paths(i,used_list)
        return used_list

    def update(self):
        self.move()
        if self.active_node.x == self.parent.stop_point[0] and self.active_node.y == self.parent.stop_point[1]:
            return False 
        print(self.active_node.x,self.active_node.y)
        return True

class Node():
    def __init__(self,x,y,parent):
        self.x = x
        self.y = y
        self.parent = parent
        self.childs = []

    def add_child(self,child):
        self.childs.append(child)