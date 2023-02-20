from base.geometries import Vector
from base.objects import Scene, Camera, Sphere

scene = Scene("../images/image3")
# camera
main_camera = Camera(16 / 9, 1920, 1)

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

scene.add_cam(main_camera)
scene.render()
