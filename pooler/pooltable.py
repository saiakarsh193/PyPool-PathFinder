from pooler.vector import Vector
from pooler.point import Point

class PoolTable:
    def __init__(self, data):
        self.ball_radius = data['metadata']['ball_radius']
        self.pocket_radius = data['metadata']['pocket_radius']
        self.table_width = data['metadata']['table_width']
        self.table_height = data['metadata']['table_height']
        self.balls = data['balls']
        for ball, value in self.balls.items():
            self.balls[ball] = Point(value)
        self.pockets = data['pockets']
        for pocket, value in enumerate(self.pockets):
            self.pockets[pocket] = Point(value)
        self.cue = self.balls['0']
        self.paths = []

    def calculatePaths(self):
        for ball in self.balls.keys():
            if(ball != '0'):
                self.paths += self.calculatePathsForBall(ball)
                break

    def calculatePathsForBall(self, ball):
        tpaths = []
        for pocket in self.pockets:
            cpath = self.calculatePathSTP(self.cue, self.balls[ball], pocket)
            if(len(cpath) > 0):
                tpaths.append(cpath)
            break
        return tpaths

    def calculatePathSTP(self, source, target, pocket):
        # print(source, '->', target, '->', pocket)
        lines = [
                Vector(source, target),
                Vector(target, pocket),
                ]
        return lines

    def getPaths(self):
        tpaths = []
        for path in self.paths:
            cpath = []
            for line in path:
                cpath.append(line.toList())
            tpaths.append(cpath)
        return tpaths

    def getLines(self):
        tpaths = self.getPaths()
        tlines = []
        for path in tpaths:
            tlines += path
        return tlines

