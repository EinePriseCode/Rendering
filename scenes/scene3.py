from geometries import Vector
from objects import Scene, Camera, Sphere

# maybe the image is a bit wider, because of a different fov due to my own implementation
scene = Scene("../images/image3")
# camera
main_camera = Camera(16 / 9, 1920, 1)

# spheres
s0 = Sphere(Vector(0, 1, -10), 4, color=Vector(1, 0, 0))
s1 = Sphere(Vector(-4, 1, -3), 1, color=Vector(0, 1, 0))
s2 = Sphere(Vector(4, 2, -3), 1, color=Vector(0, 0, 1))
s3 = Sphere(Vector(1, -.6, -1.5), .4, color=Vector(1, 1, 0))
s4 = Sphere(Vector(-1, -2, -2), .2, color=Vector(0, 1, 1))

s5 = Sphere(Vector(0, -1010, -2), 1000, color=Vector(1, 1, 1))

scene.add_render_object(s0)
scene.add_render_object(s1)
scene.add_render_object(s2)
scene.add_render_object(s3)
scene.add_render_object(s4)
scene.add_render_object(s5)

scene.add_cam(main_camera)
scene.render()
