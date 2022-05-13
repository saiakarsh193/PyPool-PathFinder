from pooler.vector import Vector
from pooler.line import Line 
from pooler.targetpoint import TP

class PoolTable:
    def __init__(self, data):
        # importing the metadata
        self.ball_radius = data['metadata']['ball_radius']
        self.pocket_radius = data['metadata']['pocket_radius']
        self.table_width = data['metadata']['table_width']
        self.table_height = data['metadata']['table_height']

        # converting ball points to vectors
        self.balls = data['balls']
        for ball, value in self.balls.items():
            self.balls[ball] = Vector(value)

        # conveting pockets to vectors with ids/names
        # pocket names
        # a  b  c
        #
        # d     e
        #
        # f  g  h
        self.pocket_names = ['a', 'c', 'h', 'f', 'b', 'g', 'e', 'd']
        self.pockets = {}
        for pocket, value in zip(self.pocket_names, data['pockets']):
            self.pockets[pocket] = Vector(value)
        
        # assigning the cue ball
        self.cue = '0'

        # max recursion depth for path finding
        self.max_depth = 3

        # counters for logging
        self.total_addchild = 1
        self.total_endps = 0

    def calculatePaths(self):
        self.proots = []
        for pocket in self.pockets.keys():
            self.proots.append(self.calculateRootForPocket(pocket))
        print('Total children calculated:', self.total_addchild)

    def calculateRootForPocket(self, pocket):
        rootpoint = TP(self.getPocketTP(pocket), pocket, None, 0, [])
        for ball in self.balls.keys():
            if(ball != self.cue):
                rootpoint.addChild(self.calculateAttackPoint(self.balls[ball], rootpoint.point), ball)
                self.total_addchild += 1
        for child in rootpoint.children:
            self.calculateTPChildren(child)
        # self.printTP(rootpoint)
        return rootpoint

    def printTP(self, rootp):
        print('cur:', rootp)
        print('chilren:')
        for child in rootp.children:
            print(child)
        print()
        for child in rootp.children:
            self.printTP(child)

    def calculateTPChildren(self, tp):
        if(tp.name == self.cue or tp.level >= self.max_depth):
            return
        for ball in self.balls.keys():
            if(ball not in tp.history):
                tp.addChild(self.calculateAttackPoint(self.balls[ball], tp.point), ball)
                self.total_addchild += 1
        for child in tp.children:
            self.calculateTPChildren(child)

    def getPocketTP(self, pocket):
        diff_vec = Vector(0, 0)
        if(pocket == 'a'):
            diff_vec = Vector(self.ball_radius, -self.ball_radius)
        return self.pockets[pocket] + diff_vec

    def calculateAttackPoint(self, source, target):
        d = target - source
        d = d / d.mag
        atp = source + d * (-2 * self.ball_radius)
        return atp

    def getPaths(self):
        paths = []
        for rootp in self.proots:
            ends = []
            stack = [rootp]
            while(len(stack) > 0):
                cur = stack.pop(-1)
                if(cur.name == self.cue):
                    ends.append(cur)
                for child in cur.children:
                    stack.append(child)
            for endpoint in ends:
                paths.append(self.makePathFromPoints(self.expandToPoints(endpoint)))
                self.total_endps += 1
        print('Total endpoints found:', self.total_endps)
        return paths

    def expandToPoints(self, tp):
        cur = tp
        epath = [cur.point]
        while(cur.parent != None):
            cur = cur.parent
            epath.append(cur.point)
        return epath

    def makePathFromPoints(self, points):
        path = []
        for i in range(len(points) - 1):
            path.append(Line(points[i], points[i + 1]))
        for ind, line in enumerate(path):
            path[ind] = line.toList()
        return path

    def getLines(self):
        tpaths = self.getPaths()
        tlines = []
        for path in tpaths:
            tlines += path
        return tlines

