class Point:
    def __init__(self, x, y=None):
        if(type(x) == list):
            self.x = x[0]
            self.y = x[1]
        else:
            self.x = x
            self.y = y

    def __str__(self):
        return 'Point({x}, {y})'.format(
            x = str(round(self.x, 3)),
            y = str(round(self.y, 3)),
        )

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

    def __mul__(self, other):
        return Point(self.x * other, self.y * other)
