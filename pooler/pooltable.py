from pooler.line import Line
import random

class PoolTable:
    def __init__(self, data):
        self.rdata = data
        self.rballs = self.rdata['balls']
        self.cue = self.rballs['0']
        self.tlines = {}

    def calculateMoves(self):
        for ball in self.rballs.keys():
            if(ball != '0'):
                self.tlines[ball] = self.calcMovesFor(ball)

    def calcMovesFor(self, target):
        return [Line(0, 0, 0, 40), Line(40, 0, 0, 40)]

    def getFrame(self):
        frame = []
        for ball, coord in self.rdata['balls'].items():
            frame.append({'type': 'ball', 'name': ball, 'x': coord[0], 'y': coord[1], 'radius': self.rdata['metadata']['ball_radius']})
        line_colors = ['red', 'blue', 'pink']
        for lines in self.tlines.values():
            cur_color = random.choice(line_colors)
            for line in lines:
                frame.append({'type': 'line', 'color': cur_color, 'x1': line.x1, 'y1': line.y1, 'x2': line.x2, 'y2': line.y2})
        return frame
