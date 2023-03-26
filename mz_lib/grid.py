import os, random, requests
from mz_lib import node

import sys
sys.setrecursionlimit(1000000)

class Grid():
    def __init__(self,problem,path_size,start_p=None,stop_p=None,maze_hardness=None):
        #path_size is a variable able to carry path or size
        # it is a var for random size when chooseing the wall or road on random maze gen if it is bigger there will be more walls
        if maze_hardness:
            self.rand_size = 2
        else:
            self.rand_size = 1
        self.nodes = {}
        if problem == 1:
            print("path yok",path_size)
            self.maze = self.read_from_url(path_size)
            self.gen_nodes()
        elif problem == 2:
            self.random_maze_gen(int(path_size[0]),int(path_size[1]),start_p,stop_p)
    #reads path and returns a maze that is able to use

    def gen_nodes(self):
        x = 0
        for row in self.maze:
            y = 0
            for col in row:
                self.nodes[(x,y)]=node.Node(x,y)
                self.nodes[(x,y)].type = self.maze[x][y]
                y+=1
            x+=1

    def change_barrier(self):
        self.set_threes(self.maze)
        self.set_two(self.maze)
        self.gen_nodes()

    def read_from_url(self,url):
        maze = []
        response = requests.get(url)
        data = response.text
        data = data.split("\n")
        top_bottom = []
        for line in data:
            top_bottom.append(1)
        top_bottom.append(1)
        top_bottom.append(1)
        maze.append(top_bottom)
        for line in data:
            if line != '':
                x=[]
                x.append(1)
                for element in line:
                    x.append(int(element))
                x.append(1)
                maze.append(x)
        maze.append(top_bottom)
        return maze

    def set_threes(self,maze):
        y = 0
        for i in maze:
            x = 0
            for j in i:
                if maze[x][y] == 3:
                    random_num = random.randint(0,4)
                    if random_num == 0:
                        self.make_T(maze,x,y)
                    elif random_num == 1:
                        self.make_L(maze,x,y)
                    else:
                        self.make_I(maze,x,y)
                x +=1
            y+=1

    def set_two(self,maze):
        y = 0
        for i in maze:
            x = 0
            for j in i:
                if maze[x][y] == 2:
                    random_num = random.randint(0,4)
                    if random_num == 0:
                        self.make_Sl(maze,x,y)
                    elif random_num == 1:
                        self.make_V(maze,x,y)
                    else:
                        self.make_H(maze,x,y)
                x +=1
            y+=1

    def make_Sl(self,maze,x,y):
        maze[x][y] = 1
        maze[x][y+1] = 1
        maze[x+1][y] = 1
        maze[x+1][y+1] = 0

    def make_V(self,maze,x,y):
        maze[x][y] = 1
        maze[x][y+1] = 1
        maze[x+1][y] = 0
        maze[x+1][y+1] = 0

    def make_H(self,maze,x,y):
        maze[x][y] = 1
        maze[x][y+1] = 0
        maze[x+1][y] = 1
        maze[x+1][y+1] = 0

    def make_L(self,maze,x,y):
        maze[x][y] = 1
        maze[x][y+1] = 1
        maze[x][y+2] = 1
        maze[x+1][y] = 1
        maze[x+1][y+1] = 0
        maze[x+1][y+2] = 0
        maze[x+2][y] = 1
        maze[x+2][y+1] = 0
        maze[x+2][y+2] = 0

    def make_T(self,maze,x,y):
        maze[x][y] = 1
        maze[x][y+1] = 1
        maze[x][y+2] = 1
        maze[x+1][y] = 0
        maze[x+1][y+1] = 1
        maze[x+1][y+2] = 0
        maze[x+2][y] = 0
        maze[x+2][y+1] = 1
        maze[x+2][y+2] = 0

    def make_I(self,maze,x,y):
        maze[x][y] = 1
        maze[x][y+1] = 1
        maze[x][y+2] = 1
        maze[x+1][y] = 0
        maze[x+1][y+1] = 1
        maze[x+1][y+2] = 0
        maze[x+2][y] = 1
        maze[x+2][y+1] = 1
        maze[x+2][y+2] = 1

    def read_generate(self,path):
        maze = []
        f = open(path,'r')
        readed = f.read()  
        readed = readed.split("\n")
        top_bottom = []
        for line in readed:
            top_bottom.append(1)
        top_bottom.append(1)
        top_bottom.append(1)
        maze.append(top_bottom)
        for line in readed:
            if line != '':
                x=[]
                x.append(1)
                for element in line:
                    x.append(int(element))
                x.append(1)
                maze.append(x)
        maze.append(top_bottom)
        f.close()
        return maze

    def gen_start_stop_on_corner(self,size_x,size_y):
        start = (0,0)
        stop = (size_x,size_y)

    def free_nbh(self,nbh_list):
        free_nbh_list = []
        for i in nbh_list:
            if i.type == 0 and not i.map_setted:
                free_nbh_list.append(i)
        return free_nbh_list

    def move_node(self,pos_x,pos_y):
        active_node = self.nodes[(pos_x,pos_y)]
        nbh_list = [self.nodes[(pos_x,pos_y+1)],self.nodes[(pos_x,pos_y-1)],
                    self.nodes[(pos_x+1,pos_y)],self.nodes[(pos_x-1,pos_y)]]
        free_nbh_list = self.free_nbh(nbh_list)
        if len(free_nbh_list)!=0:
            is_changed = False
            for i in free_nbh_list:
                random_num = random.randint(0,self.rand_size)
                if not i.map_setted:
                    if not random_num:
                        active_node.map_childs.append(i)
                        i.map_parents.append(active_node)
                        i.map_setted = True
                        is_changed = True
                        print(i.x,i.y,"ye gidiliyor")
                        self.move_node(i.x,i.y)
                    else:
                        i.type = 1
                        i.map_setted = True
                        print("1 atandı")
            if not is_changed:
                i = free_nbh_list[0]
                active_node.map_childs.append(i)
                i.map_parents.append(active_node)
                i.map_setted = True
                i.type = 0
                print("mecburi_yol")
                self.move_node(i.x,i.y)

    def zero_maze(self,size_x,size_y):
        maze = []
        for x in range(0,size_x):
            line = []
            for y in range(0,size_y):
                if x == 0 or x == size_x-1 or y == 0 or y == size_y-1:
                    line.append(1)                 
                else:
                    line.append(0)
            maze.append(line)
        return maze

    def random_maze_gen(self,size_x,size_y,start_p,stop_p):
        self.maze = self.zero_maze(size_x,size_y)
        self.gen_nodes()
        self.move_node(*start_p)
        self.not_used_setter()
        self.gen_maze()

    def is_not_middle(self,i):
        if self.nodes[i].x != 0 and self.nodes[i].x != len(self.maze)-1 and self.nodes[i].y != 0 and self.nodes[i].y != len(self.maze[0])-1:
            return True
        return False

    def not_used_setter(self):
        while self.is_none_gone():
            for i in self.nodes.keys():
                if(self.is_not_middle(i)):
                    if not self.nodes[i].map_setted:
                        nbh_list = [self.nodes[(i[0],i[1]+1)],self.nodes[(i[0],i[1]-1)],
                            self.nodes[(i[0]+1,i[1])],self.nodes[(i[0]-1,i[1])]]
                        for node in nbh_list:
                            if node.type == 1 and (self.is_not_middle((node.x,node.y))):
                                node.type = 0
                                self.move_node(node.x,node.y)
                                break

    def is_none_gone(self):
        none_gone = False
        for i in self.nodes.keys():
            if(self.is_not_middle(i)):
                if not self.nodes[i].map_setted:
                    none_gone = True
        return none_gone

    def gen_maze(self):
        for i in self.nodes.keys():
            self.maze[self.nodes[i].x][self.nodes[i].y] = self.nodes[i].type
