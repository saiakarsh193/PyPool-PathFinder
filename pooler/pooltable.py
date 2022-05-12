from pooler.line import Line
import random

class PoolTable:
    def __init__(self, data):
        self.ball_radius = data['metadata']['ball_radius']
        self.pocket_radius = data['metadata']['pocket_radius']
        self.table_width = data['metadata']['table_width']
        self.table_height = data['metadata']['table_height']
        self.balls = data['balls']
        self.pockets = data['pockets']
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
                Line(source[0], source[1], target[0], target[1]),
                Line(target[0], target[1], pocket[0], pocket[1]),
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

