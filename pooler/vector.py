import math

class Vector:
    def __init__(self, x, y=None):
        if(type(x) == list):
            self.x = x[0]
            self.y = x[1]
        else:
            self.x = x
            self.y = y
        self.mag = math.sqrt(self.x**2 + self.y**2)

    def __str__(self):
        return 'Vector({x}, {y})'.format(
            x = str(round(self.x, 3)),
            y = str(round(self.y, 3)),
        )

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y)

    def __mul__(self, other):
        return Vector(self.x * other, self.y * other)

    def __truediv__(self, other):
        return Vector(self.x / other, self.y / other)

    def equals(self, other):
        return (self.x == other.x and self.y == other.y)

    @staticmethod
    def Dot(a, b):
        return a.x * b.x + a.y * b.y

    @staticmethod
    def AngleBetween(a, b):
        return math.degrees(math.acos(Vector.Dot(a / a.mag, b / b.mag)))

