import sys

import numpy as np

from geometries import Ray, Vector
from materials import DiffuseMaterial
from rendering import Image


class Transform:
    def __init__(self, position):
        self.position = position


class RenderObject(Transform):
    def __init__(self, position, material):
        super().__init__(position)
        self.material = material

    def hit(self, ray, t_min, t_max):
        raise NotImplementedError("Please Implement this method")


class Sphere(RenderObject):
    def __init__(self, position, radius, color, material):
        super().__init__(position, material)
        self.radius = radius
        self.color = color

    def hit(self, ray, t_min, t_max):
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
            return t, pos, norm if norm * ray.direction <= 0 else norm * -1, self.color, self.material


class Camera(Transform):
    def __init__(self, focal_length, aspect_ratio, image_width, samples_per_pixel=1,
                 t_min=.001, t_max=float("inf"), max_bounce_depth=50):
        super().__init__(Vector(0, 0, 0))

        self.focal_length = focal_length
        self.samples_per_pixel = samples_per_pixel
        self.t_min = t_min
        self.t_max = t_max
        self.max_bounce_depth = max_bounce_depth

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

    def ray_color(self, ray, scene, depth):
        # no more light gathered if max bounce depth is exceeded
        if depth <= 0:
            return Vector(0, 0, 0)

        result = scene.hit(ray, self.t_min, self.t_max)
        if result is not None:
            _, pos, norm, color, material = result
            # to show normal vector as color
            # return Vector(norm.x + 1, norm.y + 1, norm.z + 1) * .5
            # target = pos + norm + Vector.rand_in_unit_sphere()
            # with older diffuse formulation
            # target = pos + Vector.rand_in_hemisphere(norm)
            # return self.ray_color(Ray(pos, target-pos), scene, depth-1) * .5
            if material is not None:
                scattered_ray, attenuation = material.scatter(ray, pos, norm, color)
                r_c = self.ray_color(scattered_ray, scene, depth - 1)
                return Vector(r_c.x * attenuation.x, r_c.y * attenuation.y, r_c.z * attenuation.z)
            else:
                # to show plain object color
                return color

        unit_dir = ray.direction.normalize()
        t = .5 * (unit_dir.y + 1)
        return Vector(1, 1, 1) * (1-t) + Vector(.5, .7, 1) * t

    def render(self, scene):
        i = Image(self.image_width, self.image_height)
        # looping through pixels for rendering
        for y in range(self.image_height)[::-1]:
            for x in range(self.image_width):
                pixel_color = Vector(0, 0, 0)
                for s in range(self.samples_per_pixel):
                    ray = self.get_ray(x, y, self.samples_per_pixel > 1)
                    pixel_color = pixel_color + self.ray_color(ray, scene, self.max_bounce_depth)
                i.image_list[y, x] = self.write_color(pixel_color).to_int_array()
            print(f"\r{1-y/self.image_height}%")
        return i

    def write_color(self, pixel_color):
        # doesn't have to be clamped because no single summed up color value is bigger then 1
        return Vector.gamma2_corrected(pixel_color / self.samples_per_pixel) * 255


class Scene:
    def __init__(self, name, path=""):
        self.name = name
        self.path = path
        self.objects = []
        self.cameras = []

    def render(self):
        for i in range(len(self.cameras)):
            img = self.cameras[i].render(self)
            if i > 0:
                img.save_image(f"{self.path}{self.name}-{i + 1}.ppm")
            else:
                img.save_image(f"{self.path}{self.name}.ppm")
            print(f"Rendered {i+1} camera!")

    def add_cam(self, cam):
        self.cameras.append(cam)

    def add_object(self, obj):
        self.objects.append(obj)

    def hit(self, ray, t_min, t_max):
        result = None
        for obj in self.objects:
            result_obj = obj.hit(ray, t_min, t_max)
            if result_obj is not None:
                if result is None or result_obj[0] < result[0]:
                    result = result_obj
        return result


scene = Scene("rendering7")
main_camera = Camera(1, 16 / 9, 1920, samples_per_pixel=4, max_bounce_depth=100)
cam2 = Camera(1, 16 / 9, 1920, samples_per_pixel=2, max_bounce_depth=2)
cam3 = Camera(1, 16 / 9, 1920, samples_per_pixel=2, max_bounce_depth=4)
cam4 = Camera(1, 16 / 9, 1920, samples_per_pixel=2, max_bounce_depth=8)
cam5 = Camera(1, 16 / 9, 1920, samples_per_pixel=2, max_bounce_depth=16)

scene.add_cam(main_camera)
# scene.add_cam(cam2)
# scene.add_cam(cam3)
# scene.add_cam(cam4)
# scene.add_cam(cam5)

s0 = Sphere(Vector(0, 0, -3), 1, Vector(1, 0, 0), DiffuseMaterial(Vector(99/255, 132/255, 117/255)))
s1 = Sphere(Vector(0, -51, -3), 50, Vector(0, 0, 1), DiffuseMaterial(Vector(218/255, 247/255, 220/255)))
# s2 = Sphere(Vector(-1, 0, -10), 3, Vector(0, 0, 0))
# s3 = Sphere(Vector(-2, 1, -2), .2, Vector(1, 0, 0))
# s4 = Sphere(Vector(0, -1, -2), 1, Vector(0, 1, 0))

scene.add_object(s0)
scene.add_object(s1)
# scene.add_object(s2)
# scene.add_object(s3)
# scene.add_object(s4)

scene.render()


