from pygame.math import Vector2
import math
# Returns a new contact object of the correct subtype
# This function has been done for you.
def generate(a, b, **kwargs):
    # Check if a's type comes later than b's alphabetically.
    # We will label our collision types in alphabetical order, 
    # so the lower one needs to go first.
    if b.contact_type < a.contact_type:
        a, b = b, a
    # This calls the class of the appropriate name based on the two contact types.
    return globals()[f"{a.contact_type}_{b.contact_type}"](a, b, **kwargs)
    

# Generic contact class, to be overridden by specific scenarios
class Contact():
    def __init__(self, a, b, resolve=False, **kwargs):
        self.a = a
        self.b = b
        self.kwargs = kwargs
        self.update()
        if resolve:
            self.resolve(update=False)
 
    def update(self): 
        self.overlap = 0
        self.normal = Vector2(0,0) 

    def resolve(self, restitution=None, friction=None, update=True):
        if update:
            self.update()
        if restitution is None:
            if "restitution" in self.kwargs.keys():
                restitution = self.kwargs["restitution"]
            else:
                restitution = 0
        if friction is None:
            if "friction" in self.kwargs.keys():
                friction = self.kwargs["friction"]
            else:
                friction = 0


        # resolve overlap
        if self.overlap>0:
            a = self.a
            b = self.b
            m=1/(1/a.mass + 1/b.mass)
            a.delta_pos(m/a.mass*self.overlap*self.normal)
            b.delta_pos(-m/b.mass*self.overlap*self.normal)
            # resolve velocity
            point=self.point
            va = a.vel + a.avel * (point()-a.pos).rotate(90)
            vb = b.vel + b.avel * (point()-b.pos).rotate(90)
            v = va-vb
            vn = v.dot(self.normal)
            if vn < 0:
                rebound = 0
                Jn = -(1+restitution)*m*v.dot(self.normal)
                tangent=self.normal.rotate(90)
                vt=v.dot(tangent)
                vts=math.copysign(1.0,vt)
                Jt=-m*vt
                if abs(Jt) > friction*Jn:
                    Jt=-vts*friction*Jn
                else:
                    
                    pass
                impulse = Jn * self.normal + Jt*tangent
                a.impulse(impulse)
                b.impulse(-impulse)

    def point(self):
        return Vector2(0,0)

# Contact class for two circles
class Circle_Circle(Contact):
    def __init__(self, a, b, **kwargs):
        super().__init__(a, b, **kwargs)

    def update(self):  # compute the appropriate values
        r=self.a.pos-self.b.pos
        self.overlap = self.a.radius+self.b.radius-r.magnitude()
        if r.magnitude()==0:
            self.normal=Vector2(0,0)
        else:
            self.normal = r.normalize()

    def point(self):
        return self.a.pos-(self.a.radius*self.normal)


# Contact class for Circle and a Wall
# Circle is before Wall because it comes before it in the alphabet
class Circle_Wall(Contact):
    def __init__(self, a, b, **kwargs):
        self.circle = a
        self.wall = b
        super().__init__(a, b, **kwargs)

    def update(self):  # compute the appropriate values
        self.overlap = self.circle.radius + (self.wall.pos - self.circle.pos).dot(self.wall.normal)
        self.normal = self.wall.normal


# Empty class for Wall - Wall collisions
# The intersection of two infinite walls is not interesting, so skip them
class Wall_Wall(Contact):
    def __init__(self, a, b, **kwargs):
        super().__init__(a, b, **kwargs)




class Circle_Polygon(Contact):
    def __init__(self, a, b, **kwargs):
        self.circle = a
        self.polygon = b
        super().__init__(a, b, **kwargs)

    def print(self):
        return self.circle.pos - self.circle.radius*self.normal

    def update(self):  # compute the appropriate values
        min_overlap=math.inf

        for i in range(len(self.polygon.points)):
            self.polygon.points[i]
        
        #loop over all sides find index of minimum overlap
        for i, (wall_point, wall_normal) in enumerate(zip(self.polygon.points, self.polygon.normals)):
            overlap = self.circle.radius  + (wall_point - self.circle.pos).dot(wall_normal)
            # if overlap is less than min_overlap
            if overlap < min_overlap:
                #update min_overlap
                min_overlap = overlap
                #save index
                index=i

        self.overlap = min_overlap
        self.normal = self.polygon.normals[index]
        
        if 0 < self.overlap < self.circle.radius:
            #check if the point is beyond one of the endpoints
            endpoint1 = self.polygon.points[index]
            endpoint2 = self.polygon.points[index-1]
            if (self.circle.pos - endpoint1).dot(endpoint1-endpoint2) > 0:
                r = self.circle.pos - endpoint1
                self.overlap = self.circle.radius - r.magnitude()
                self.normal=r.normalize()
            elif(self.circle.pos - endpoint2).dot(endpoint2 - endpoint1) > 0:
                r = self.circle.pos - endpoint2
                self.overlap = self.circle.radius - r.magnitude()
                self.normal=r.normalize()

    def point(self):
        return self.circle.pos-(self.circle.radius*self.normal)

#the contact point is the circle position-(radius* normal )