from geometries import Vector
from materials import DiffuseMaterial
from objects import Scene, Camera, Sphere

# maybe the image is a bit wider, because of a different fov due to my own implementation
scene = Scene("../images/image4")
# camera
cam0 = Camera(16 / 9, 400, 1, samples_per_pixel=1)
cam1 = Camera(16 / 9, 400, 1, lookfrom=Vector(0, 15, -8), lookat=Vector(0, 0, -8), vup=Vector(0, 0, 1), samples_per_pixel=1)
# cam2 = Camera(16 / 9, 400, 1, lookfrom=Vector(0, -4, 0), lookat=Vector(0, -4, -1), samples_per_pixel=1)
# cam1 = Camera(16 / 9, 1920, 1, samples_per_pixel=2)
# cam2 = Camera(16 / 9, 1920, 1, samples_per_pixel=4)
# cam3 = Camera(16 / 9, 1920, 1, samples_per_pixel=8)
# cam4 = Camera(16 / 9, 1920, 1, samples_per_pixel=16)

# spheres
s0 = Sphere(Vector(0, -1, -13), 4, color=Vector(1, 0, 0))
s1 = Sphere(Vector(-8, -2, -10), 3, color=Vector(0, 1, 0))
s2 = Sphere(Vector(4, -3, -8), 2, color=Vector(0, 0, 1))
s3 = Sphere(Vector(10, 0, -14), 5, color=Vector(0, 1, 1))

s4 = Sphere(Vector(0, -1005, -2), 1000, color=Vector(.9, .9, .9))

s5 = Sphere(Vector(-5.5, -4, -5.5), 1, color=Vector(1, .84, 0))
s6 = Sphere(Vector(-3, -3, -7.8), 2, color=Vector(.85, .85, .85))
s7 = Sphere(Vector(4, -4, -4.9), 1, color=Vector(.75, .54, .44))

s8 = Sphere(Vector(0, -2, -3.8), 2.8, color=Vector(0, 0, 0))
s9 = Sphere(Vector(0, -2, -3.8), 2.6, color=Vector(0, 0, 0))
s10 = Sphere(Vector(-13, 3, -18), 8, color=Vector(0, 0, 0))

s11 = Sphere(Vector(0, 0, -40), 20, color=Vector(1, 1, 0))
s12 = Sphere(Vector(25, 8, -20), 5, color=Vector(1, 1, 0))
s13 = Sphere(Vector(1, -4.5, -7.3), .5, color=Vector(1, 1, 0))

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
scene.add_cam(cam1)
# scene.add_cam(cam2)
# scene.add_cam(cam3)
# scene.add_cam(cam4)

scene.render()
