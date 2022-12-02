from pygame.math import Vector2
import pygame
import math

class PhysicsObject:
    def __init__(self, pos, vel=(0,0), mass=1, angle=0, avel=0, momi=math.inf):
        self.pos=Vector2(pos)
        self.vel=Vector2(vel)
        self.mass=mass
        self.angle=angle
        self.avel=avel
        self.momi=momi
        self.clear_force()

    def clear_force(self):
        self.force=Vector2(0,0)
        self.torque=0

    def add_force(self, force):
        self.force+=force

    def add_torque(self, torque):
        self.torque += torque

    def update(self, dt):
        # update velocity using the current force
        self.vel += (self.force/self.mass)*dt
        # update position using the newly updated velocity
        self.pos += self.vel * dt

        self.avel+=self.torque/self.momi *dt
        self.angle+=self.avel*dt

    def delta_pos(self, delta):
        self.pos += delta

    def impulse(self, impulse):
        self.vel += (impulse/self.mass)

class Circle(PhysicsObject):
    def __init__(self, window, radius=100, color=(255,255,255), width=0, **kwargs):
        
        self.window = window
        self.radius = radius
        self.color = color
        self.width = width
        self.contact_type="Circle"
        super().__init__(**kwargs)

    def draw(self):
        pygame.draw.circle(self.window, self.color, self.pos, self.radius, self.width)

class Wall(PhysicsObject):
    def __init__(self, window, start_point, end_point, reverse=False, color=(255,255,255), width=1, **kwargs):
        self.start_point = Vector2(start_point)
        self.end_point = Vector2(end_point)
        self.window = window
        self.color = color
        self.width = width
        self.reverse = reverse
        self.contact_type = "Wall"
        super().__init__(pos=(self.start_point + self.end_point)/2, mass=math.inf)
        self.update_wall()

    def update_wall(self):
        self.pos = (self.start_point + self.end_point)/2
        self.normal = (self.end_point - self.start_point).rotate(90).normalize()
        if self.reverse:
            self.normal*= -1


    def draw(self):
        pygame.draw.line(self.window, self.color, self.start_point, self.end_point, self.width)

    

class Polygon(PhysicsObject):
    def __init__(self, window, local_points=[], color=(255,0,0), width=0, **kwargs):
        self.window=window
        self.color=color
        self.width=width
        self.contact_type= "Polygon"
        super().__init__(**kwargs)

        #save local points as vecotr2 objects
        self.local_points = []
        for i in local_points:
            self.local_points.append(Vector2(i))
        self.points = self.local_points.copy()

        #calculate normals local_normals
        self.local_normals = []
        for i in range(len(self.local_points)):
            normal = (self.local_points[i] - self.local_points[i-1]).normalize().rotate(90)
            self.local_normals.append(normal)
        self.normals = self.local_normals.copy()

        self.update_polygon()

    def update_polygon(self):
        for i, p in enumerate(self.local_points):
            self.points[i] = self.pos + p.rotate_rad(self.angle)
            self.normals[i] = self.local_normals[i].rotate_rad(self.angle)

    def update(self, dt):
        super().update(dt)
        self.update_polygon()

    def delta_pos(self, delta):
        super().delta_pos(delta)
        self.update_polygon()
    
    def draw(self):
        pygame.draw.polygon(self.window, self.color, self.points, self.width)
        # for p,n in zip(self.points,self.normals):
        #     pygame.draw.line(self.window, (255,255,255), p, p+50*n)


