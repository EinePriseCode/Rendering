import numpy as np


class Vector:

    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __add__(self, v):
        return Vector(self.x + v.x, self.y + v.y, self.z + v.z)

    def __sub__(self, v):
        return Vector(self.x - v.x, self.y - v.y, self.z - v.z)

    def __mul__(self, l):
        if type(l) is Vector:
            return self.x * l.x + self.y * l.y + self.z * l.z
        else:
            return Vector(self.x * l, self.y * l, self.z * l)

    def __truediv__(self, l):
        return Vector(self.x * 1/l, self.y * 1/l, self.z * 1/l)

    def __floordiv__(self, l):
        return Vector(self.x * 1 // l, self.y * 1 // l, self.z * 1 // l)

    def length(self):
        return np.sqrt(self.x ** 2 + self.y ** 2 + self.z ** 2)

    def normalize(self):
        l = self.length()
        return self.__truediv__(l)

    def cross(self, v):
        return Vector(self.y * v.z - v.y * self.z, self.z * v.x - v.z * self.x, self.x * v.y - v.x * self.y)

    def __str__(self):
        return f"{self.x} {self.y} {self.z}"

    def to_int_array(self):
        # rounded for more correct colors (but cast to int to \void floats in ppm file)
        return [int(np.around(self.x)), int(np.around(self.y)), int(np.around(self.z))]

    def near_zero(self):
        s = 1e-8
        return self.x < s and self.y < s and self.z < s

    def reflect(self, norm):
        return self - norm * (self * norm) * 2

    # right-handed coordinate system, x right, y left, z backwards
    @staticmethod
    def up():
        return Vector(0, 1, 0)

    @staticmethod
    def down():
        return Vector(0, -1, 0)

    @staticmethod
    def left():
        return Vector(-1, 0, 0)

    @staticmethod
    def right():
        return Vector(1, 0, 0)

    @staticmethod
    def forward():
        return Vector(0, 0, -1)

    @staticmethod
    def backward():
        return Vector(0, 0, 1)

    @staticmethod
    def null():
        return Vector(0, 0, 0)

    @staticmethod
    def rand_in_unit_sphere():
        while True:
            v = Vector.rand(-1, 1)
            if v.length() >= 1:
                continue
            return v.normalize()

    @staticmethod
    def rand_in_hemisphere(norm):
        in_unit_sphere = Vector.rand_in_unit_sphere()
        if in_unit_sphere * norm > 0:
            return in_unit_sphere
        else:
            return in_unit_sphere * -1

    @staticmethod
    def rand(low, high):
        return Vector(np.random.uniform(low, high),
                      np.random.uniform(low, high),
                      np.random.uniform(low, high))

    @staticmethod
    def gamma2_corrected(v):
        # element-wise square root
        return Vector(np.sqrt(v.x), np.sqrt(v.y), np.sqrt(v.z))


class Ray:
    def __init__(self, origin, direction):
        self.origin = origin
        self.direction = direction

    def get_position(self, t):
        return self.origin + self.direction * t
