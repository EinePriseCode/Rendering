from geometries import Vector, Ray


class Material:
    def __init__(self, albedo):
        self.albedo = albedo

    def scatter(self, ray, pos, norm, color):
        raise NotImplementedError("Please Implement this method")


class DiffuseMaterial(Material):
    def scatter(self, ray, pos, norm, color):
        scatter_dir = norm + Vector.rand_in_unit_sphere()
        if scatter_dir.near_zero():
            scatter_dir = norm
        return Ray(pos, scatter_dir), self.albedo


class SpecularMaterial(Material):
    def scatter(self, ray, pos, norm, color):
        reflect_dir = ray.direction.normalize().reflect(norm)
        # no direction calculation necessary because ray and normal are always in opposite directions
        return Ray(pos, reflect_dir), self.albedo
