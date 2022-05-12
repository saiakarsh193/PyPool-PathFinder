class Line:
    def __init__(self, x1, y1, x2, y2):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

    def __str__(self):
        return 'Line[({x1}, {y1}) -> ({x2}, {y2})]'.format(
            x1 = str(round(self.x1, 3)),
            y1 = str(round(self.y1, 3)),
            x2 = str(round(self.x2, 3)),
            y2 = str(round(self.y2, 3)),
        )

    def toList(self):
        return [self.x1, self.y1, self.x2, self.y2]
