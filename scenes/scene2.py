from objects import Scene, Camera

# maybe the image is a bit wider, because of a different fov due to my own implementation
scene = Scene("../images/image2")
# camera
main_camera = Camera(16 / 9, 1920, 1)

scene.add_cam(main_camera)
scene.render()
