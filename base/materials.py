import numpy as np

from base.geometries import Vector, Ray


class Material:

    def emitted(self):
        return Vector(0, 0, 0)

    # super class for materials: offering an abstract scatter method
    def scatter(self, ray, pos, norm, front_face):
        raise NotImplementedError("Please Implement this method")


class DiffuseMaterial(Material):
    def __init__(self, albedo):
        self.albedo = albedo

    # implementation of a diffuse material (inherits from Material)
    def scatter(self, ray, pos, norm, front_face):
        # returns a new ray from hit position in random (scattered) direction and color of material
        scatter_dir = norm + Vector.rand_in_unit_sphere().normalize()
        if scatter_dir.near_zero():
            scatter_dir = norm
        return Ray(pos, scatter_dir), self.albedo


class SpecularMaterial(Material):
    # implementation of a specular material (inherits from Material)
    def __init__(self, albedo, fuzz):
        self.albedo = albedo
        # adds fuzz factor for specular materials
        # < or <= makes no big difference (fuzz-vector length is smaller than 1 at all)
        self.fuzz = fuzz if fuzz <= 1 else 1

    def scatter(self, ray, pos, norm, front_face):
        # returns a new ray from hit position in reflection direction (plus random fuzz direction)
        # and color of material
        reflect_dir = ray.direction.normalize().reflect(norm)
        scattered_dir = reflect_dir + (Vector.rand_in_unit_sphere() * self.fuzz)
        if scattered_dir * norm > 0:
            return Ray(pos, scattered_dir), self.albedo
        return None


class TransmissiveMaterial(Material):
    def __init__(self, ior):
        self.ior = ior

    def scatter(self, ray, pos, norm, front_face):
        refraction_ratio = 1/self.ior if front_face else self.ior

        unit_direction = ray.direction.normalize()

        cos_theta = np.amin([(unit_direction*-1)*norm, 1])
        sin_theta = np.sqrt(1.0 - cos_theta * cos_theta)

        if refraction_ratio * sin_theta > 1 or self.reflectance(cos_theta, refraction_ratio) > np.random.uniform(0, 1):
            scattered_dir = unit_direction.reflect(norm)
        else:
                scattered_dir = unit_direction.refract(norm, cos_theta, refraction_ratio)

        return Ray(pos, scattered_dir), Vector(1, 1, 1)

    @staticmethod
    def reflectance(cosine, ref_idx):
        # Schlick's approximation for reflectance
        r0 = (1-ref_idx) / (1+ref_idx)
        r0 = r0**2
        return r0 + (1-r0) * (1-cosine)**5


class EmissiveMaterial(Material):
    def __init__(self, color, intensity):
        self.color = color
        self.intensity = intensity

    def scatter(self, ray, pos, norm, front_face):
        return None

    def emitted(self):
        return self.emit()

    # emits light with color and intensity
    def emit(self):
        return self.color * self.intensity

