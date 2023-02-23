from base.geometries import Vector
from base.materials import DiffuseMaterial, SpecularMaterial, Transmissive, Emissive
from base.objects import Scene, Camera, Sphere

scene = Scene("../images/image8")
# camera
cam0 = Camera(16 / 9, 1920, 1, max_bounce_depth=64, samples_per_pixel=64,
              background_gradient=(Vector(0, 0, 0), Vector(0, 0, 0)))

# spheres
s0 = Sphere(Vector(0, -1, -13), 4, material=DiffuseMaterial(Vector(1, 0, 0)))
s1 = Sphere(Vector(-8, -2, -10), 3, material=DiffuseMaterial(Vector(0, 1, 0)))
s2 = Sphere(Vector(4, -3, -8), 2, material=DiffuseMaterial(Vector(0, 0, 1)))
s3 = Sphere(Vector(10, 0, -14), 5, material=DiffuseMaterial(Vector(0, 1, 1)))

s4 = Sphere(Vector(0, -1005, -2), 1000, material=DiffuseMaterial(Vector(.9, .9, .9)))

s5 = Sphere(Vector(-5.5, -4, -5.5), 1, material=SpecularMaterial(Vector(1, .84, 0), 0))
s6 = Sphere(Vector(-3, -3, -7.8), 2, material=SpecularMaterial(Vector(.85, .85, .85), 0))
s7 = Sphere(Vector(4, -4, -4.9), 1, material=SpecularMaterial(Vector(.75, .54, .44), .5))

s8 = Sphere(Vector(0, -2, -3.8), 2.8, material=Transmissive(1.5))
s9 = Sphere(Vector(0, -2, -3.8), -2.7, material=Transmissive(1.5))
s10 = Sphere(Vector(-13, 3, -18), 8, material=Transmissive(1.325))

s11 = Sphere(Vector(0, 0, -40), 20, material=Emissive(Vector(1, 1, 1), 1))
s12 = Sphere(Vector(25, 8, -20), 5, material=Emissive(Vector(.95, .62, 0.09), 1))
s13 = Sphere(Vector(1, -4.5, -7.3), .5, material=Emissive(Vector(1, 1, 1), 1))

scene.add_render_object(s0)
scene.add_render_object(s1)
scene.add_render_object(s2)
scene.add_render_object(s3)
scene.add_render_object(s4)

scene.add_render_object(s5)
scene.add_render_object(s6)
scene.add_render_object(s7)

scene.add_render_object(s8)
scene.add_render_object(s9)
scene.add_render_object(s10)

scene.add_render_object(s11)
scene.add_render_object(s12)
scene.add_render_object(s13)

scene.add_cam(cam0)

scene.render()
