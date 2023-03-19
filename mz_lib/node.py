class Node():
    def __init__(self,x,y,depth=-1,parent=None):
        self.x = x
        self.y = y
        self.type = -1
        self.parent = parent
        self.childs = []
        self.depth = depth
        self.is_saw = False
        self.is_used = False
        self.is_moved = False
        self.real_depth = -1
        self.is_short_way = False
        self.in_way = None
        self.out_way = None
        self.map_childs = []
        self.map_parents = []
        self.map_setted = False
        self.barren = False
        self.barren_p = None
        self.barren_c = None
        self.g_real_depth = -1
        self.g_saw = False
        self.is_game_short_way = False

    def add_child(self,child):
        self.childs.append(child)