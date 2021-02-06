import math

class Vector2(object):
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y
    
    def __str__(self):
        return "("+str(self.x) + ", " + str(self.y) +")"

    def asTuple(self):
        return self.x, self.y
        
    def asInt(self):
        return int(self.x), int(self.y)

    def __add__(self, other):
        return Vector2(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vector2(self.x - other.x, self.y - other.y)

    def __mul__(self, scalar):
        return Vector2(self.x * scalar, self.y * scalar)
    
    def magnitude_squared(self):
        return self.x**2 + self.y**2

    def magnitude(self):
        return sqrt(self.magnitude_squared())
    
    def is_parallel(self, other):
        if self.x != 0 and other.x != 0:
            factor = self.x / other.x
            if other.y * factor == self.y:
                return True
            else:
                return False
        elif self.y != 0 and other.y != 0:
            factor = self.y / other.y
            if other.x * factor == self.x:
                return True
            else:
                return False
        else:
            return False

    def normalize(self):
        if self.x == 0 and self.y == 0:
            return self
        _sum = abs(self.x) + abs(self.y)
        return Vector2(self.x / _sum, self.y / _sum)