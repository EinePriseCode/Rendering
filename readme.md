

# Engine part: Building scene/environment for rendering (camera, spheres, etc.)
scene = Scene("rendering13")
# cameras
main_camera = Camera(130, Vector(-1, 0, 1).length(), 16 / 9, 512, Vector(-1, 0, 1), Vector(0, 0, 0),
                     samples_per_pixel=16, max_bounce_depth=16, aperture=.2)
# cam2 = Camera(130, 1, 16 / 9, 1920, samples_per_pixel=2, max_bounce_depth=2)
# cam3 = Camera(130, 1, 16 / 9, 1920, samples_per_pixel=2, max_bounce_depth=4)
# cam4 = Camera(130, 1, 16 / 9, 1920, samples_per_pixel=2, max_bounce_depth=8)
# cam5 = Camera(130, 1, 16 / 9, 1920, samples_per_pixel=2, max_bounce_depth=16)

scene.add_cam(main_camera)
# scene.add_cam(cam2)
# scene.add_cam(cam3)
# scene.add_cam(cam4)
# scene.add_cam(cam5)

# spheres
s0 = Sphere(Vector(2, 0, 1), 1, Vector(1, 0, 0), SpecularMaterial(Vector(255 / 255, 215 / 255, 0 / 255), 0))
s1 = Sphere(Vector(-1.8, -.2, -2), .8, Vector(1, 0, 0), SpecularMaterial(Vector(216 / 255, 216 / 255, 216 / 255), .3))
s2 = Sphere(Vector(+1.8, -.2, -2), .8, Vector(1, 0, 0), Transmissive(1.5))
s3 = Sphere(Vector(+1.8, -.2, -2), -.6, Vector(1, 0, 0), Transmissive(1.5))

s4 = Sphere(Vector(0, 1, -1.2), -.4, Vector(1, 0, 0), Emissive(Vector(240/255, 248/255, 255/255), 1))

s5 = Sphere(Vector(0, -101, -2), 100, Vector(0, 0, 1), Emissive(Vector(240/255, 248/255, 255/255), 1))
# s2 = Sphere(Vector(-1, 0, -10), 3, Vector(0, 0, 0))
# s3 = Sphere(Vector(-2, 1, -2), .2, Vector(1, 0, 0))
# s4 = Sphere(Vector(0, -1, -2), 1, Vector(0, 1, 0))

scene.add_render_object(s0)
scene.add_render_object(s1)
scene.add_render_object(s2)
scene.add_render_object(s3)
scene.add_render_object(s4)
scene.add_render_object(s5)
# scene.add_object(s3)
# scene.add_object(s4)

# start rendering
scene.render()