from geometries import Vector, Ray


class Material:
    def scatter(self, ray, pos, norm, color):
        raise NotImplementedError("Please Implement this method")


class DiffuseMaterial(Material):
    def __init__(self, albedo):
        self.albedo = albedo

    def scatter(self, ray, pos, norm, color):
        scatter_dir = norm + Vector.rand_in_unit_sphere()
        if scatter_dir.near_zero():
            scatter_dir = norm
        return Ray(pos, scatter_dir), self.albedo
