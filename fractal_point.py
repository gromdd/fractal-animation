import numpy as np

class point():

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        return point(self.x+other.x, self.y+other.y)

    def __sub__(self, other):
        return point(self.x-other.x, self.y-other.y)

    def __mul__(self, other):
        return point(self.x*other, self.y*other)

    def length(self):
        return np.sqrt(self.x**2+self.y**2)

    def rotation_90_deg(self):
        return point(-self.y, self.x)

    def __repr__(self):
        return(str((self.x, self.y)))
    
