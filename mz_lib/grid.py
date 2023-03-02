import os
from mz_lib import node

class Grid():
    def __init__(self,path):
        self.mazle = [
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

        if os.path.exists(path):
            print("path var",path)
            self.mazle = self.read_generate(path)
            self.gen_nodes()
        else:
            print("path yok",path)
            #self.mazle = self.generate(path)
    #reads path and returns a mazle that is able to use

    def gen_nodes(self):
        y = 0
        for row in self.mazle:
            x = 0
            for col in row:
                self.nodes[(x,y)]=node.Node(x,y)
                self.nodes[(x,y)].type = self.mazle[x][y]
                x+=1
            y+=1
        print(self.nodes)

    def read_generate(self,path):
        mazle = []
        f = open(path,'r')
        readed = f.read()  
        readed = readed.split("\n")
        for line in readed:
            if line != '':
                x=[]
                for element in line:
                    x.append(int(element))
                mazle.append(x)
        f.close()
        return mazle

    def generate(self,size):
        pass