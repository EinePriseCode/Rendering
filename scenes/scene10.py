from base.geometries import Vector
from base.materials import DiffuseMaterial, SpecularMaterial, Transmissive, Emissive
from base.objects import Scene, Camera, Sphere

scene = Scene("../images/image10")

lookfrom = Vector(20, 3, 4)
lookat = Vector(0, -1, -13)

focus_distance = (lookfrom - lookat).length()

cam0 = Camera(16 / 9, 1920, focus_distance, max_bounce_depth=64, samples_per_pixel=64,
              lookfrom=lookfrom, lookat=lookat, vup=Vector(0, 1, 0), aperture=.2)

cam1 = Camera(16 / 9, 1920, focus_distance, max_bounce_depth=64, samples_per_pixel=64,
              lookfrom=lookfrom, lookat=lookat, vup=Vector(0, 1, 0), aperture=.5)

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

s14 = Sphere(Vector(10, -2, 2), 3, material=SpecularMaterial(Vector(0, 0, 0), .1))
s15 = Sphere(Vector(16, -3, 0), 2, material=SpecularMaterial(Vector(1, 1, 1), .2))
s16 = Sphere(Vector(-8, -2, 1), 3, material=DiffuseMaterial(Vector(1, .83, .61)))
s17 = Sphere(Vector(0, 1, 5), 6, material=DiffuseMaterial(Vector(.6, 1, .6)))
s18 = Sphere(Vector(-13, -4.2, -1), .8, material=DiffuseMaterial(Vector(1, .7, .4)))

s19 = Sphere(Vector(18, -4, -6), 1, material=Transmissive(1.5))
s20 = Sphere(Vector(10, -4.6, -5), .4, material=DiffuseMaterial(Vector(0, .2, .2)))
s21 = Sphere(Vector(12, -4.7, -7), .3, material=DiffuseMaterial(Vector(1, .6, 1)))

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

scene.add_render_object(s14)
scene.add_render_object(s15)
scene.add_render_object(s16)
scene.add_render_object(s17)
scene.add_render_object(s18)

scene.add_render_object(s19)
scene.add_render_object(s20)
scene.add_render_object(s21)

scene.add_cam(cam0)
scene.add_cam(cam1)

scene.render()
