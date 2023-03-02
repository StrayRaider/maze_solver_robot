class Node():
    def __init__(self,x,y,depth=-1,parent=None):
        self.x = x
        self.y = y
        self.parent = parent
        self.childs = []
        self.depth = depth
        self.is_saw = False
        self.is_used = False
        self.is_moved = False
        self.real_depth = -1
        self.robot_here = False

    def add_child(self,child):
        self.childs.append(child)