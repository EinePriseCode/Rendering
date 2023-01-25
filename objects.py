import numpy as np

from geometries import Ray, Vector
from rendering import Image


class Transform:
    def __init__(self, position):
        self.position = position


class Sphere(Transform):
    def __init__(self, position, radius, color):
        super().__init__(position)
        self.radius = radius
        self.color = color

    def hit_sphere(self, ray, t_min=1, t_max=1000):
        pointer = ray.origin - self.position

        # less efficient
        # a = ray.direction * ray.direction
        # b = (pointer * ray.direction) * 2
        # c = pointer * pointer - self.radius ** 2

        a = ray.direction * ray.direction
        half_b = (pointer * ray.direction)
        c = pointer * pointer - self.radius ** 2

        discriminant = half_b ** 2 - a * c

        if discriminant < 0:
            return None
        else:
            sqrtd = np.sqrt(discriminant)
            t = (-half_b - sqrtd) / a

            # filter out t if out of range
            if t < t_min or t > t_max:
                t = (-half_b + sqrtd) / a
                if t < t_min or t > t_max:
                    return None

            pos = ray.get_position(t)
            norm = (ray.get_position(t) - self.position).normalize()
            # <= because norm should point out if norm and ray are orthogonal
            return t, pos, norm if norm * ray.direction <= 0 else norm * -1, self.color


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

    def get_ray(self, x, y, antialiasing):
        rand_offset_x, rand_offset_y = 0, 0
        if antialiasing:
            # why only one direction noise
            rand_offset_x = np.random.uniform(0, 1)
            rand_offset_y = np.random.uniform(0, 1)
        return Ray(self.position, self.lower_left_corner
                   + self.horizontal * (x + rand_offset_x) / (self.image_width - 1)
                   + self.vertical * (y + rand_offset_y) / (self.image_height - 1) - self.position)

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
                for s in range(self.samples_per_pixel):
                    ray = self.get_ray(x, y, self.samples_per_pixel > 1)
                    pixel_color = pixel_color + self.ray_color(ray, objects)
                i.image_list[y, x] = self.average_color(pixel_color).to_int_array()

        return i

    def average_color(self, pixel_color):
        # doesn't have to be clamped because no single summed up color value is bigger then 255
        # floor division to avoid float colors
        return pixel_color // self.samples_per_pixel
