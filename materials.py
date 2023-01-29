from geometries import Vector, Ray


class Material:
    # super class for materials: offering an albedo color and an abstract scatter method
    def __init__(self, albedo):
        self.albedo = albedo

    def scatter(self, ray, pos, norm, color):
        raise NotImplementedError("Please Implement this method")


class DiffuseMaterial(Material):
    # implementation of a diffuse material (inherits from Material)
    def scatter(self, ray, pos, norm, color):
        # returns a new ray from hit position in random (scatterd) direction and color of material
        scatter_dir = norm + Vector.rand_in_unit_sphere()
        if scatter_dir.near_zero():
            scatter_dir = norm
        return Ray(pos, scatter_dir), self.albedo


class SpecularMaterial(Material):
    # implementation of a specular material (inherits from Material)
    def __init__(self, albedo, fuzz):
        super().__init__(albedo)
        # adds fuzz factor for specular materials
        # < or <= makes no big difference (fuzz-vector length is smaller than 1 at all)
        self.fuzz = fuzz if fuzz <= 1 else 1

    def scatter(self, ray, pos, norm, color):
        # returns a new ray from hit position in reflection direction (plus random fuzz direction)
        # and color of material
        reflect_dir = ray.direction.normalize().reflect(norm)
        scattered_dir = reflect_dir + (Vector.rand_in_unit_sphere() * self.fuzz)
        if scattered_dir * norm > 0:
            return Ray(pos, scattered_dir), self.albedo
        return None
