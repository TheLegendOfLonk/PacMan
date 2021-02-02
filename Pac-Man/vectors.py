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

    def __mul__(self, scalar):
        return Vector2(self.x * scalar, self.y * scalar)
    
    def is_parallel(self, other):
        try:
            factor = self.x / other.x
            if other.y * factor == self.y:
                return True
            else:
                return False
        except ZeroDivisionError:
            return False