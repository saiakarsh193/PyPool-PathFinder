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

    def calculatePathsForBall(self, ball):
        tpaths = []
        for pocket in self.pockets:
            cpath = self.calculatePathSTP(self.cue, self.balls[ball], pocket)
            if(len(cpath) > 0):
                tpaths.append(cpath)
        return tpaths

    def calculatePathSTP(self, source, target, pocket):
        # print(source, '->', target, '->', pocket)
        lines = [Line(0, 0, 0, 40), Line(40, 0, 0, 40)]
        return lines

    def getFrame(self):
        frame = []
        for ball, coord in self.balls.items():
            frame.append({'type': 'ball', 'name': ball, 'x': coord[0], 'y': coord[1], 'radius': self.ball_radius})
        line_colors = ['red', 'blue', 'black', 'purple', 'white']
        for path in self.paths:
            cur_color = random.choice(line_colors)
            for line in path:
                frame.append({'type': 'line', 'color': cur_color, 'x1': line.x1, 'y1': line.y1, 'x2': line.x2, 'y2': line.y2})
        return frame
