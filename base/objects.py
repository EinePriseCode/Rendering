import sys

import numpy as np

from base.geometries import Ray, Vector
from base.rendering import Image

sys.setrecursionlimit(1500)


class Transform:
    # base class for objects in scene
    def __init__(self, position):
        # position in scene
        self.position = position


class RenderObject(Transform):
    # superclass for all objects which can be rendered by a camera (inherits from Transform)
    def __init__(self, position, material):
        super().__init__(position)
        # add material to an object
        self.material = material

    def hit(self, ray, t_min, t_max):
        # RenderObjects can be hit by camera/render ray (abstract method)
        # returns tuple of (ray parameter t, intersection position, normal of surface in point,
        # color and material of object)
        raise NotImplementedError("Please Implement this method")


class Sphere(RenderObject):
    def __init__(self, position, radius, color=Vector.null(), material=None):
        super().__init__(position, material)
        # adds a radius (and a color) to a RenderObject
        self.radius = radius
        self.color = color

    def hit(self, ray, t_min, t_max):
        # implements hit method for spheres
        pointer = ray.origin - self.position

        # less efficient
        # a = ray.direction * ray.direction
        # b = (pointer * ray.direction) * 2
        # c = pointer * pointer - self.radius ** 2

        # solving system of linear equations from vector based intersection
        a = ray.direction * ray.direction
        half_b = (pointer * ray.direction)
        c = pointer * pointer - self.radius ** 2

        discriminant = half_b ** 2 - a * c

        if discriminant < 0:
            return None
        else:
            sqrtd = np.sqrt(discriminant)
            # calculating ray parameter t
            t = (-half_b - sqrtd) / a

            # filter out t if out of range
            if t < t_min or t > t_max:
                t = (-half_b + sqrtd) / a
                if t < t_min or t > t_max:
                    return None

            # getting intersection point and normal in this point
            pos = ray.get_position(t)
            norm = (ray.get_position(t) - self.position) / self.radius
            # <= because norm should point out if norm and ray are orthogonal
            front_face = norm * ray.direction <= 0
            return t, pos, norm if front_face else norm * -1, front_face, self.color, self.material


class Camera(Transform):
    def __init__(self, aspect_ratio, image_width, focal_length, fov=130,
                 lookfrom=Vector(0, 0, 0), lookat=Vector(0, 0, -1), vup=Vector(0, 1, 0),
                 samples_per_pixel=1, t_min=.001, t_max=float("inf"), max_bounce_depth=50,
                 background_gradient=(Vector(1, 1, 1), Vector(.5, .7, 1)), aperture=0.0):
        super().__init__(lookfrom)

        self.background_gradient = background_gradient

        self.fov = fov
        self.focal_length = focal_length
        self.samples_per_pixel = samples_per_pixel
        self.t_min = t_min
        self.t_max = t_max
        self.max_bounce_depth = max_bounce_depth

        self.aspect_ratio = aspect_ratio

        self.image_width = image_width
        self.image_height = int(self.image_width // self.aspect_ratio)

        # width depends on fov and focal length
        self.viewport_width = 2 * np.tan(np.radians(self.fov)/2) * self.focal_length
        self.viewport_height = self.viewport_width * 1/self.aspect_ratio

        # calculate orthonormal basis of camera coordinate system
        w = (lookfrom - lookat).normalize()
        self.u = vup.cross(w).normalize()
        self.v = w.cross(self.u)

        self.direction = w * -1

        self.horizontal = self.u * self.viewport_width
        self.vertical = self.v * self.viewport_height

        self.lens_radius = aperture / 2

        self.lower_left_corner = (self.position + self.direction * self.focal_length
                                  - self.vertical/2 - self.horizontal/2)

    def get_ray(self, x, y, antialiasing):
        # antialiasing offset
        rand_offset_x, rand_offset_y = 0, 0
        # depth of field offset (lens)
        lens_offset = Vector.rand_in_unit_disc() * self.lens_radius
        position_offset = self.u * lens_offset.x + self.v * lens_offset.y

        if antialiasing:
            rand_offset_x = np.random.uniform(0, 1)
            rand_offset_y = np.random.uniform(0, 1)

        return Ray(self.position + position_offset, self.lower_left_corner
                   + self.horizontal * (x + rand_offset_x) / (self.image_width - 1)
                   + self.vertical * (y + rand_offset_y) / (self.image_height - 1) - self.position - position_offset)

    def ray_color(self, ray, scene, depth):
        # no more light gathered if max bounce depth is exceeded
        if depth <= 0:
            return Vector.null()

        result = scene.hit(ray, self.t_min, self.t_max)
        if result is not None:
            _, pos, norm, front_face, color, material = result
            # to show normal vector as color
            # return Vector(norm.x + 1, norm.y + 1, norm.z + 1) * .5
            # target = pos + norm + Vector.rand_in_unit_sphere()
            # with older diffuse formulation
            # target = pos + Vector.rand_in_hemisphere(norm)
            # return self.ray_color(Ray(pos, target-pos), scene, depth-1) * .5
            if material is not None:
                scatter_result = material.scatter(ray, pos, norm, front_face)
                emitted_result = material.emitted()

                if scatter_result is not None:
                    scattered_ray, attenuation = scatter_result
                    r_c = self.ray_color(scattered_ray, scene, depth - 1)
                    return emitted_result + Vector(r_c.x * attenuation.x, r_c.y * attenuation.y, r_c.z * attenuation.z)
                else:
                    return emitted_result
            else:
                # to show plain object color
                return color

        unit_dir = ray.direction.normalize()
        t = .5 * (unit_dir.y + 1)
        return self.background_gradient[0] * (1 - t) + self.background_gradient[1] * t

    def render(self, scene):
        i = Image(self.image_width, self.image_height)
        # looping through pixels for rendering
        for y in range(self.image_height)[::-1]:
            for x in range(self.image_width):
                pixel_color = Vector.null()
                for s in range(self.samples_per_pixel):
                    ray = self.get_ray(x, y, self.samples_per_pixel > 1)
                    pixel_color = pixel_color + self.ray_color(ray, scene, self.max_bounce_depth)
                i.image_list[y, x] = self.write_color(pixel_color).to_int_array()
            print(f"\r{(1-y/self.image_height)*100:.2f}%")
        return i

    def write_color(self, pixel_color):
        # doesn't have to be clamped because no single summed up color value is bigger then 1
        return Vector.gamma2_corrected(pixel_color / self.samples_per_pixel) * 255


class Scene:
    # a scene represents an environment by carrying cameras and render_objects
    def __init__(self, name, path=""):
        self.name = name
        self.path = path

        # lists of objects for rendering
        self.render_objects = []
        self.cameras = []

    def render(self):
        # rendering of scene is calling render method of all cameras
        for i in range(len(self.cameras)):
            # rendering image
            img = self.cameras[i].render(self)
            # saving image
            if i > 0:
                img.save_image(f"{self.path}{self.name}-{i + 1}.ppm")
            else:
                img.save_image(f"{self.path}{self.name}.ppm")
            print(f"Rendered {i+1} camera!")

    def add_cam(self, cam):
        # adds a Camera to scene
        self.cameras.append(cam)

    def add_render_object(self, obj):
        # adds RenderObject to scene
        self.render_objects.append(obj)

    def hit(self, ray, t_min, t_max):
        # returns information about a hit/intersection of a ray with a render object
        # (scene checks instead of camera to enable more use cases)
        result = None
        # checks for hit for all render objects
        for obj in self.render_objects:
            result_obj = obj.hit(ray, t_min, t_max)

            # returns a result only if it was a hit and if hit object is closer to camera than others
            if result_obj is not None:
                if result is None or result_obj[0] < result[0]:
                    result = result_obj
        return result



