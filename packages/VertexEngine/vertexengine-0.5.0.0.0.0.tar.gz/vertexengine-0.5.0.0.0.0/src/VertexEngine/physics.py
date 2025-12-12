# physics.py
import math

class Vector2:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def __add__(self, o): return Vector2(self.x + o.x, self.y + o.y)
    def __sub__(self, o): return Vector2(self.x - o.x, self.y - o.y)
    def __mul__(self, s): return Vector2(self.x * s, self.y * s)

    def length(self):
        return math.sqrt(self.x**2 + self.y**2)

    def normalize(self):
        l = self.length()
        return Vector2(self.x/l, self.y/l) if l != 0 else Vector2()


class Body:
    def __init__(self, mass=1, position=Vector2(), velocity=Vector2()):
        self.mass = mass
        self.position = position
        self.velocity = velocity
        self.forces = Vector2()

    def apply_force(self, force):
        self.forces += force

    def integrate(self, dt):
        acc = Vector2(self.forces.x / self.mass, self.forces.y / self.mass)

        self.velocity += acc * dt
        self.position += self.velocity * dt

        self.forces = Vector2()


class PhysicsWorld:
    def __init__(self, gravity=Vector2(0, 9.8)):
        self.gravity = gravity
        self.bodies = []

    def add_body(self, body):
        self.bodies.append(body)
        return body

    def step(self, dt):
        for b in self.bodies:
            b.apply_force(self.gravity * b.mass)
            b.integrate(dt)
