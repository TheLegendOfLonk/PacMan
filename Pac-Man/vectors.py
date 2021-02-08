'''
Contains the Vector2 class
'''

import math

class Vector2(object):
    '''
    A class used to implement 2D Vectors

    Attributes
    ----------
    x : float
        The x-cordinate of the Vector
    y : float
        The y-cordinate of the Vector

    Methods
    -------
    as_tuple()
        Represents Vector2 as tuple of floats
    as_int()
        Represents Vector2 as tuple of integers
    magnitude_squared()
        Retruns the squared magnitude of Vector2
    magnitude()
        Returns the magnitude of Vector2
    is_parallel(other)
        Checks whether given Vector2 and self are parallel
    normalize()
        Returns normalized Vector2
    '''
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def __str__(self):
        return "("+str(self.x) + ", " + str(self.y) +")"

    def __add__(self, other):
        return Vector2(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vector2(self.x - other.x, self.y - other.y)

    def __mul__(self, scalar):
        return Vector2(self.x * scalar, self.y * scalar)

    def as_tuple(self):
        '''
        Represents Vector2 as tuple

        Returns
        -------
        tuple
            A tuple of floats
        '''
        return self.x, self.y

    def as_int(self):
        '''
        Represents Vector2 as tuple of integer

        Returns
        -------
        tuple
            A tuple of integers
        '''
        return int(self.x), int(self.y)

    def magnitude_squared(self):
        '''
        Gets the squared magnitude of vector

        Retruns
        -------
        float
            The squared magnitude
        '''
        return self.x**2 + self.y**2

    def magnitude(self):
        '''
        Gets the magnitude of vector

        Returns
        -------
        float
            Magnitude of vector
        '''
        return math.sqrt(self.magnitude_squared())

    def is_parallel(self, other):
        '''
        Checks whether self and given vector are parallel

        Parameters
        ----------
        other : Vector2
            The other vector

        Returns
        -------
        bool
            True if given vector is parallel to self and False if not
        '''
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
        '''
        Normalizes self so that the magnitude equals 1

        Returns
        -------
        Vector2
            The normalized vector
        '''
        if self.x == 0 and self.y == 0:
            return self
        _sum = abs(self.x) + abs(self.y)
        return Vector2(self.x / _sum, self.y / _sum)
