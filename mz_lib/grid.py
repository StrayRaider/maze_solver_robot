import os, random, requests
from mz_lib import node

class Grid():
    def __init__(self,problem,path_size):
        self.maze = [
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0 ,0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0 ,0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 1, 0, 1, 1, 1, 1, 0, 1, 0 ,0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0 ,0, 0, 0, 1, 0, 1, 1, 1, 1],
        [1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 0 ,0, 0, 0, 1, 0, 0, 0, 0, 0],
        [1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0 ,0, 0, 0, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0 ,0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0 ,0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
]
        self.nodes = {}
        if problem == 1:
            if os.path.exists(path_size):
                print("path var",path_size)
                self.maze = self.read_generate(path_size)
                #self.maze = self.random_maze_gen(15,15)
                self.maze = self.read_generate("./mz_lib/maps/url1.txt")
            else:
                print("path yok",path_size)
                self.maze = self.read_from_url(path_size)

        elif problem == 2:
            self.maze = self.random_maze_gen(int(path_size[0]),int(path_size[1]))
        self.gen_nodes()
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
        print(self.nodes)

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
        print("maze : ",maze)
        return maze

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

    #yol usulü çalışsak ? örneğin x = 4, 9 değerleri 0 içeren yatay yollar olsa
    # 3, 11 de dikey yollar olsa ve bunların çevre yolları bol 1 içerse
    def random_maze_gen(self,size_x,size_y):
        maze = []
        for x in range(0,size_x):
            line = []
            for y in range(0,size_y):
                rand = random.randint(0,3)
                print(rand)
                if x == 0 or x == size_x-1 or y == 0 or y == size_y-1:
                    line.append(1)
                elif not rand:
                    line.append(1)                    
                else:
                    line.append(0)
            maze.append(line)
        print(maze)
        return maze