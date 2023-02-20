from base.geometries import Vector
from base.materials import DiffuseMaterial, SpecularMaterial, Transmissive
from base.objects import Scene, Camera, Sphere

scene = Scene("../images/image7")
# camera
cam0 = Camera(16 / 9, 1920, 1, max_bounce_depth=1, samples_per_pixel=64)
cam1 = Camera(16 / 9, 1920, 1, max_bounce_depth=2, samples_per_pixel=64)
cam2 = Camera(16 / 9, 1920, 1, max_bounce_depth=4, samples_per_pixel=64)
cam3 = Camera(16 / 9, 1920, 1, max_bounce_depth=8, samples_per_pixel=64)
cam4 = Camera(16 / 9, 1920, 1, max_bounce_depth=16, samples_per_pixel=64)

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
s9 = Sphere(Vector(0, -2, -3.8), 2.6, material=Transmissive(1.5))
s10 = Sphere(Vector(-13, 3, -18), 8, material=Transmissive(1.5))

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

scene.add_cam(cam0)
scene.add_cam(cam1)
scene.add_cam(cam2)
scene.add_cam(cam3)
scene.add_cam(cam4)

scene.render()
