import math

class Line:
    def __init__(self, a, b):
        self.a = a
        self.b = b
        self.mag = math.sqrt((a.x - b.x)**2 + (a.y - b.y)**2)

    def __str__(self):
        return 'Line[{a} -> {b}]'.format(
            a = self.a,
            b = self.b
        )

    def toList(self):
        return [self.a.x, self.a.y, self.b.x, self.b.y]
