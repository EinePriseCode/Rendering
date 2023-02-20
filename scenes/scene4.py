from base.geometries import Vector
from base.objects import Scene, Camera, Sphere

scene = Scene("../images/image4")
# camera
cam0 = Camera(16 / 9, 1920, 1, samples_per_pixel=1)
cam1 = Camera(16 / 9, 1920, 1, samples_per_pixel=2)
cam2 = Camera(16 / 9, 1920, 1, samples_per_pixel=4)
cam3 = Camera(16 / 9, 1920, 1, samples_per_pixel=8)
cam4 = Camera(16 / 9, 1920, 1, samples_per_pixel=16)

# spheres
s0 = Sphere(Vector(0, -1, -13), 4, color=Vector(1, 0, 0))
s1 = Sphere(Vector(-8, -2, -10), 3, color=Vector(0, 1, 0))
s2 = Sphere(Vector(4, -3, -8), 2, color=Vector(0, 0, 1))
s3 = Sphere(Vector(10, 0, -14), 5, color=Vector(0, 1, 1))

s4 = Sphere(Vector(0, -1005, -2), 1000, color=Vector(.9, .9, .9))

scene.add_render_object(s0)
scene.add_render_object(s1)
scene.add_render_object(s2)
scene.add_render_object(s3)
scene.add_render_object(s4)

scene.add_cam(cam0)
scene.add_cam(cam1)
scene.add_cam(cam2)
scene.add_cam(cam3)
scene.add_cam(cam4)

scene.render()
