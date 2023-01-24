import numpy as np


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
            return t, pos, (ray.get_position(t) - self.position).normalize(), self.color

