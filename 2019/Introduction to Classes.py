class Circle:
    pi = 3.1415

    def __init__(self, radius, center):
        self.radius = radius
        self.center = center
    
    @property
    def diameter(self):
        """The diameter property."""
        return self.radius*2
    @diameter.setter
    def diameter(self, value):
        self.radius = value/2

    @property
    def center(self):
        """The center property."""
        return self._center
    @center.setter
    def center(self, value):
        self._center = value

    
    def p(self):
        return 2*self.pi*self.radius

    def area(self):
        return self.pi*self.radius*self.radius

    def __repr__(self):
        return ("Circle radius = {}, center = {}, diameter = {}, perimeter = {},"
            " area = {}").format(self.radius, self.center, self.diameter self.p(), self.area())


class Rectangle:
    def __init__(self, center, w, h):
        self.center = center
        self.w = w
        self.h = h

    def p(self):
        return 2*self.w+2*self.h

    def area(self):
        return self.w*self.h
    
    def points(self):
        x, y = self.center
        left = x-self.w/2
        right = x+self.w/2
        top = y-self.h/2
        bottom = y+self.h/2
        return [(left, top), (right, top), (right, bottom), (left, bottom)]

    def __repr__(self):
        return ("Rectangle  center = {}, width = {},"
            " height = {}, perimeter = {}, area = {}").format(self.center, self.w, self.h, self.p(), self.area())

class RegularPolygon:
    def __init__(self, center, lenght, nSides):
        self.center = center
        self.length = lenght
        self.nSides = nSides
    
    def perimeter(self):
        return self.nSides * self.length

    def internalAngle(self):
        return (self.nSides-2)*180/self.nSides

    def __repr__(self):
        return ("RegularPolygon  center = {}, length = {},"
            " number of sides = {}, perimeter = {}, internal angle = {}"
            "").format(self.center, self.w, self.h, self.perimeter(), self.internalAngle())


c1 = Circle(10, (2, 2))
r1=  Rectangle((5,5), 10, 10)
# c1.r = 10
# c1.center = (15, 20)

print(c1)
print(r1.points())