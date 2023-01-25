import numpy as np

from objects import Transform, Sphere
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
        # WARNING: casts to int
        return [int(self.x), int(self.y), int(self.z)]

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

    @staticmethod
    def null():
        return Vector(0, 0, 0)


class Ray:
    def __init__(self, origin, direction):
        self.origin = origin
        self.direction = direction

    def get_position(self, t):
        return self.origin + self.direction * t


class Camera(Transform):
    def __init__(self, focal_length, aspect_ratio, image_width, samples_per_pixel=1, t_min=1, t_max=1000):
        super().__init__(Vector(0, 0, 0))

        self.focal_length = focal_length
        self.samples_per_pixel = samples_per_pixel
        self.t_min = t_min
        self.t_max = t_max

        self.aspect_ratio = aspect_ratio

        self.image_width = image_width
        self.image_height = int(self.image_width // self.aspect_ratio)

        self.viewport_height = 2.0
        self.viewport_width = self.viewport_height * self.aspect_ratio

        self.direction = Vector.forward()

        self.horizontal = Vector.right() * self.viewport_width
        self.vertical = Vector.up() * self.viewport_height

        self.lower_left_corner = (self.position + self.direction * self.focal_length
                                  - self.vertical/2 - self.horizontal/2)

    def get_ray(self, x, y):
        return Ray(self.position, self.lower_left_corner + self.horizontal * x / (self.image_width - 1)
                                                         + self.vertical * y / (self.image_height - 1) - self.position)

    def ray_color(self, ray, objects):
        result = None
        for obj in objects:
            result_obj = obj.hit_sphere(ray, self.t_min, self.t_max)
            if result_obj is not None:
                if result is None or result_obj[0] < result[0]:
                    result = result_obj

        if result is not None:
            _, pos, n, color = result
            # to show normal vector as color
            # return Vector(n.x + 1, n.y + 1, n.z + 1) * .5 * 255
            return color

        unit_dir = ray.direction.normalize()
        t = .5 * (unit_dir.y + 1)
        return Vector(255, 255, 255) * (1-t) + Vector(np.floor(255 * .5), np.floor(255 * .7), 255) * t

    def render(self, objects):
        i = Image(self.image_width, self.image_height)
        # looping through pixels for rendering
        for y in range(self.image_height)[::-1]:
            for x in range(self.image_width):
                pixel_color = Vector(0, 0, 0)
                for i in range(self.samples_per_pixel):
                    ray = self.get_ray(x, y)
                    pixel_color = pixel_color + self.ray_color(ray, objects)
                i.image_list[y, x] = self.average_color(pixel_color).to_int_array()

        return i

    def average_color(self, pixel_color):
        # doesnt have to be clamped because no single summed up color value is bigger then 255
        # floor division to avoid float colors
        return pixel_color // self.samples_per_pixel


class Scene:
    def __init__(self, name, path=""):
        self.name = name
        self.path = path
        self.objects = []
        self.cameras = []

    def render(self):
        for i in range(len(self.cameras)):
            img = self.cameras[i].render(self.objects)
            if i > 0:
                img.save_image(f"{self.path}{self.name}-{i + 1}.ppm")
            else:
                img.save_image(f"{self.path}{self.name}.ppm")

    def add_cam(self, cam):
        self.cameras.append(cam)

    def add_object(self, obj):
        self.objects.append(obj)


scene = Scene("rendering3")
main_camera = Camera(1, 16/9, 1920)
scene.add_cam(main_camera)

s0 = Sphere(Vector(0, 0, -3), 1, Vector(123, 213, 132))
s1 = Sphere(Vector(3, 2, -7), .5, Vector(0, 0, 255))
s2 = Sphere(Vector(-1, 0, -10), 3, Vector(0, 0, 0))
s3 = Sphere(Vector(-2, 1, -2), .2, Vector(255, 0, 0))
s4 = Sphere(Vector(0, -1000, -800), 1000, Vector(0, 255, 0))

scene.add_object(s0)
scene.add_object(s1)
scene.add_object(s2)
scene.add_object(s3)
scene.add_object(s4)

scene.render()




