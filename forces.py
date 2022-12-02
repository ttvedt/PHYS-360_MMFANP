import pygame
from pygame.math import Vector2
import itertools
import math

class SingleForce:
    def __init__(self, objects_list=[]):
        self.objects_list = objects_list

    def apply(self):
        for obj in self.objects_list:
            force = self.force(obj)
            obj.add_force(force)

    def force(self, obj): # virtual function
        return Vector2(0, 0)


class PairForce:
    def __init__(self, objects_list=[]):
        self.objects_list = objects_list

    def apply(self):
        # Loop over all pairs of objects and apply the calculated force
        going_list = []
        # combinationslist = []
        # Use two nested for loops (taking care to do each pair once)
        for a in self.objects_list:
            for b in self.objects_list:
                if a != b:
                    if (b,a) not in going_list:
                        going_list.append((a,b))
                        force = self.force(a,b)
        # to each object, respecting Newton's 3rd Law.  
                        a.add_force(force)
                        b.add_force(-force)

    def force(self, a, b): # virtual function
        return Vector2(0, 0)


class BondForce:
    def __init__(self, pairs_list=[]):
        # pairs_list has the format [[obj1, obj2], [obj3, obj4], ... ]
        self.pairs_list = pairs_list

    def apply(self):
        # Loop over all pairs from the pairs list.  
        for a, b in self.pairs_list:
            force= self.force(a,b)
        # Apply the force to each member of the pair respecting Newton's 3rd Law.
            a.add_force(force)
            b.add_force(-force)

    def force(self, a, b): # virtual function
        return Vector2(0, 0)

# Add Gravity, SpringForce, SpringRepulsion, AirDrag

class Spring(BondForce):
    def __init__(self, sConst = 0, nLength = 0, dampeningConst = 0, **kwargs):
        self.K = sConst
        self.L = nLength
        self.B = dampeningConst
        super().__init__(**kwargs)

    def force(self, a, b):
        r = a.pos - b.pos
        rMag = r.magnitude()
        rHat = r.normalize()
        v = a.vel - b.vel
        force = ((-self.K*(rMag-self.L) - self.B*v.dot(rHat))*rHat)
        return force

class SpringRepulsion(BondForce):
    def __init__(self, sConst = 0, nLength = 0, **kwargs):
        self.K = sConst
        self.L = nLength
        super().__init__(**kwargs)

    def force(self, a, b):
        r = a.pos - b.pos
        rMag = r.magnitude()
        rHat = r.normalize()
        if a.radius+b.radius-rMag > 0:
            force=self.K*(a.radius+b.radius-rMag)*rHat
        else:
            force=Vector2(0,0)
        return force


class Gravitation(PairForce):
    def __init__(self, G=0, **kwargs):
        self.G=G
        super().__init__(**kwargs)
    
    def mag(self, r):
        return(math.sqrt(r[0]*r[0]+r[1]*r[1]))

    def force(self, a, b):
        r= a.pos - b.pos
        return -self.G*a.mass*b.mass/self.mag(r)**3*r
    
class Gravity(SingleForce):
    def __init__(self, acc=(0,0), **kwargs):
        self.acc = Vector2(acc)
        super().__init__(**kwargs)

    def force(self, obj):
        if obj.mass == math.inf:
            obj.vel = Vector2(0,0)
            return Vector2(0,0)
        else:
            return obj.mass*self.acc
        # Note: this will throw an error if the object has infinite mass.
        # Think about how to handle those.
    
class airDrag(SingleForce):
    def __init__(self, density = 0, dragCoefficient = 0, **kwargs):
        self.drag=dragCoefficient
        self.rho = density
        super().__init__(**kwargs)

    def apply(self):
        for obj in self.objects_list:
            force = 1/100000000 * obj.vel * obj.vel.magnitude()
            obj.add_force(force)
