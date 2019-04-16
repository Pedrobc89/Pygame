class Circle:
    def __init__(self, center, radius):
        self.center = center
        self.radius = radius

    @property
    def diameter(self):
        """Diameter of the circle"""
        return self.radius*2
    @diameter.setter
    def diameter(self, value):
        self.radius = value/2

    def getDiameter(self):
        return self.radius*2
    
    def setDiameter(self, value):
        self.radius = value/2


c = Circle((2, 2), 4)
print(c.getDiameter())
c.diameter = 3
print(c.diameter)