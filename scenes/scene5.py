from geometries import Vector
from materials import DiffuseMaterial
from objects import Scene, Camera, Sphere

# maybe the image is a bit wider, because of a different fov due to my own implementation
scene = Scene("../images/image5")
# camera
cam0 = Camera(16 / 9, 1920, 1, max_bounce_depth=1, samples_per_pixel=64)
cam1 = Camera(16 / 9, 1920, 1, max_bounce_depth=2, samples_per_pixel=64)
cam2 = Camera(16 / 9, 1920, 1, max_bounce_depth=4, samples_per_pixel=64)
cam3 = Camera(16 / 9, 1920, 1, max_bounce_depth=8, samples_per_pixel=64)
cam4 = Camera(16 / 9, 1920, 1, max_bounce_depth=16, samples_per_pixel=64)

# spheres
s0 = Sphere(Vector(0, 1, -10), 4, material=DiffuseMaterial(Vector(1, 0, 0)))
s1 = Sphere(Vector(-4, 1, -3), 1, material=DiffuseMaterial(Vector(0, 1, 0)))
s2 = Sphere(Vector(4, 2, -3), 1, material=DiffuseMaterial(Vector(0, 0, 1)))
s3 = Sphere(Vector(1, -.6, -1.5), .4, material=DiffuseMaterial(Vector(1, 1, 0)))
s4 = Sphere(Vector(-1, -2, -2), .2, material=DiffuseMaterial(Vector(0, 1, 1)))
s5 = Sphere(Vector(0, -1010, -2), 1000, material=DiffuseMaterial(Vector(1, 1, 1)))

scene.add_render_object(s0)
scene.add_render_object(s1)
scene.add_render_object(s2)
scene.add_render_object(s3)
scene.add_render_object(s4)
scene.add_render_object(s5)

scene.add_cam(cam0)
scene.add_cam(cam1)
scene.add_cam(cam2)
scene.add_cam(cam3)
scene.add_cam(cam4)

scene.render()
