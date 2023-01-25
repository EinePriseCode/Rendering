from geometries import Vector
from objects import Sphere, Camera


class Scene:
    def __init__(self, name, path=""):
        self.name = name
        self.path = path
        self.objects = []
        self.cameras = []

    def render(self):
        for i in range(len(self.cameras)):
            img = self.cameras[i].render(self.objects)
            if i > 0:
                img.save_image(f"{self.path}{self.name}-{i + 1}.ppm")
            else:
                img.save_image(f"{self.path}{self.name}.ppm")

    def add_cam(self, cam):
        self.cameras.append(cam)

    def add_object(self, obj):
        self.objects.append(obj)


scene = Scene("rendering5")
main_camera = Camera(1, 16/9, 100)
cam2 = Camera(1, 16/9, 100, samples_per_pixel=2)
cam3 = Camera(1, 16/9, 100, samples_per_pixel=4)
cam4 = Camera(1, 16/9, 100, samples_per_pixel=8)
cam5 = Camera(1, 16/9, 100, samples_per_pixel=16)

scene.add_cam(main_camera)
scene.add_cam(cam2)
scene.add_cam(cam3)
scene.add_cam(cam4)
scene.add_cam(cam5)

s0 = Sphere(Vector(0, 0, -3), 1, Vector(123, 213, 132))
s1 = Sphere(Vector(3, 2, -7), .5, Vector(0, 0, 255))
s2 = Sphere(Vector(-1, 0, -10), 3, Vector(0, 0, 0))
s3 = Sphere(Vector(-2, 1, -2), .2, Vector(255, 0, 0))
s4 = Sphere(Vector(0, -1000, -800), 1000, Vector(0, 255, 0))

scene.add_object(s0)
scene.add_object(s1)
scene.add_object(s2)
scene.add_object(s3)
scene.add_object(s4)

scene.render()




