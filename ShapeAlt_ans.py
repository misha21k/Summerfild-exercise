"""
This module provides the Point and Circle classes.

>>> point = Point()
>>> point
Point(0, 0)
>>> point.x = 12
>>> str(point)
'(12, 0)'
>>> a = Point(3, 4)
>>> b = Point(3, 4)
>>> a == b
True
>>> a == point
False
>>> a != point
True

>>> circle = Circle(2)
>>> circle
Circle(2, 0, 0)
>>> circle.radius = 3
>>> circle.x = 12
>>> circle
Circle(3, 12, 0)
>>> a = Circle(4, 5, 6)
>>> b = Circle(4, 5, 6)
>>> a == b
True
>>> a == circle
False
>>> a != circle
True
"""

import math


class Point:

    def __init__(self, x=0, y=0):
        """A 2D cartesian coordinate

        >>> point = Point()
        >>> point
        Point(0, 0)
        """
        self.x = x
        self.y = y


    @property
    def distance_from_origin(self):
        """The distance of the point from the origin

        >>> point = Point(3, 4)
        >>> point.distance_from_origin
        5.0
        """
        return math.hypot(self.x, self.y)


    def __eq__(self, other):
        return self.x == other.x and self.y == other.y


    def __repr__(self):
        return ("{0.__class__.__name__}({0.x!r}, {0.y!r})".format(
                self))


    def __str__(self):
        return "({0.x!r}, {0.y!r})".format(self)


    def __add__(self, other):
        """Returns new Point whose coordinates are the sum of this one's
        and other one's

        >>> q = Point(5, -2)
        >>> r = Point(-1, 3)
        >>> p = q + r
        >>> p
        Point(4, 1)
        """
        return Point(self.x + other.x, self.y + other.y)


    def __iadd__(self, other):
        """Adds coordinates second Point object in first

        >>> p = Point(5, 7)
        >>> p += Point(1, -3)
        >>> p
        Point(6, 4)
        """
        self.x += other.x
        self.y += other.y
        return self


    def __sub__(self, other):
        """Returns new Point whose coordinates are the difference of this one's
        and other one's

        >>> q = Point(23, 15)
        >>> r = Point(0, -5)
        >>> p = q - r
        >>> p
        Point(23, 20)
        """
        return Point(self.x - other.x, self.y - other.y)


    def __isub__(self, other):
        """Subtracts coordinates second Point object from first

        >>> p = Point(4, -8)
        >>> q = Point(2, 1)
        >>> p -= q
        >>> p
        Point(2, -9)
        """
        self.x -= other.x
        self.y -= other.y
        return self


    def __mul__(self, other):
        """Returns new Point whose coordinates are the product of one and
        number

        >>> p = Point(-5, -3)
        >>> r = p * 3
        >>> r
        Point(-15, -9)
        """
        return Point(self.x * other, self.y * other)


    def __imul__(self, other):
        """Multiplies coordinates of Point and number

        >>> p = Point(3, 2)
        >>> p *= 2
        >>> p
        Point(6, 4)
        """
        self.x *= other
        self.y *= other
        return self


    def __truediv__(self, other):
        """Returns new Point whose coordinates are divided by number

        >>> p = Point(-3, 3)
        >>> q = p / 2
        >>> q
        Point(-1.5, 1.5)
        """
        return Point(self.x / other, self.y / other)


    def __itruediv__(self, other):
        """Divides Points coordinates by number

        >>> p = Point(3, 2)
        >>> p /= 2
        >>> p
        Point(1.5, 1.0)
        """
        self.x /= other
        self.y /= other
        return self


    def __floordiv__(self, other):
        """Returns new Point whose coordinates are divided by number
        without remainder

        >>> p = Point(11, 23)
        >>> q = p // 3
        >>> q
        Point(3, 7)
        """
        return Point(self.x // other, self.y // other)


    def __ifloordiv__(self, other):
        """Divides Points coordinates by number

        >>> p = Point(23, 15)
        >>> p //= 4
        >>> p
        Point(5, 3)
        """
        self.x //= other
        self.y //= other
        return self


class Circle(Point):

    def __init__(self, radius, x=0, y=0):
        """A Circle

        >>> circle = Circle(2)
        >>> circle
        Circle(2, 0, 0)
        """
        super().__init__(x, y)
        self.radius = radius


    @property
    def area(self):
        """The circle's area

        >>> circle = Circle(3)
        >>> a = circle.area
        >>> int(a)
        28
        """
        return math.pi * (self.radius ** 2)


    @property
    def edge_distance_from_origin(self):
        """The distance of the circle's edge from the origin

        >>> circle = Circle(2, 3, 4)
        >>> circle.edge_distance_from_origin
        3.0
        """
        return abs(self.distance_from_origin - self.radius)


    @property
    def circumference(self):
        """The circle's circumference

        >>> circle = Circle(3)
        >>> d = circle.circumference
        >>> int(d)
        18
        """
        return 2 * math.pi * self.radius


    @property
    def radius(self):
        """The circle's radius

        >>> circle = Circle(-2)
        Traceback (most recent call last):
        ...
        AssertionError: radius must be nonzero and non-negative
        >>> circle = Circle(4)
        >>> circle.radius = -1
        Traceback (most recent call last):
        ...
        AssertionError: radius must be nonzero and non-negative
        >>> circle.radius = 6
        """
        return self.__radius

    @radius.setter
    def radius(self, radius):
        assert radius > 0, "radius must be nonzero and non-negative"
        self.__radius = radius


    def __eq__(self, other):
        return self.radius == other.radius and super().__eq__(other)


    def __repr__(self):
        return ("{0.__class__.__name__}({0.radius!r}, {0.x!r}, "
                "{0.y!r})".format(self))


if __name__ == "__main__":
    import doctest
    doctest.testmod()