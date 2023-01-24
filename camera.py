import numpy as np

from rendering import Image


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

    def length(self):
        return np.sqrt(self.x ** 2 + self.y ** 2 + self.z ** 2)

    def normalize(self):
        l = self.length()
        return self.__truediv__(l)

    def cross(self, v):
        return Vector(self.y * v.z - v.y * self.z, self.z * v.x - v.z * self.x, self.x * v.y - v.x * self.y)

    def __str__(self):
        return f"{self.x} {self.y} {self.z}"

    def to_array(self):
        return [self.x, self.y, self.z]

    # right handed coordinate system, x right, y left, z backwards
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


class Ray:
    def __init__(self, origin, direction):
        self.origin = origin
        self.direction = direction

    def get_position(self, t):
        return self.origin + t * self.direction


class Camera:
    def __init__(self, focal_length, aspect_ratio, image_width):
        self.focal_length = focal_length
        self.aspect_ratio = aspect_ratio

        self.image_width = image_width
        self.image_height = int(self.image_width // self.aspect_ratio)

        self.viewport_height = 2.0
        self.viewport_width = self.viewport_height * self.aspect_ratio

        self.position = Vector(0, 0, 0)
        self.direction = Vector.forward()

        self.horizontal = Vector.right() * self.viewport_width
        self.vertical = Vector.up() * self.viewport_height

        self.lower_left_corner = (self.position + self.direction * self.focal_length
                                  - self.vertical/2 - self.horizontal/2)

    def get_ray(self, x, y):
        return Ray(self.position, self.lower_left_corner + self.horizontal * x / (self.image_width - 1)
                                                         + self.vertical * y / (self.image_height - 1) - self.position)

    def ray_color(self, ray):
        unit_dir = ray.direction.normalize()
        t = .5 * (unit_dir.y + 1)
        return Vector(255, 255, 255) * (1-t) + Vector(np.floor(255 * .5), np.floor(255 * .7), 255) * t

    def render(self):
        i = Image(self.image_width, self.image_height)
        # looping through pixels for rendering
        for y in range(self.image_height):
            for x in range(self.image_width):
                ray = self.get_ray(x, y)
                i.image_list[y, x] = self.ray_color(ray).to_array()

        return i


cam = Camera(1, 16/9, 300)
img = cam.render()
img.save_image("rendering2.ppm")
