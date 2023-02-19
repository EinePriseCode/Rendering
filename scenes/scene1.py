from geometries import Vector
from rendering import Image

''' for a image of static color this code is easier than using 
    the camera model with complex features (e.g. gamma correction) '''
image = Image(1920, 1080)
for y in range(image.height)[::-1]:
    for x in range(image.width):
        image.image_list[y, x] = Vector(128, 64, 255).to_int_array()

image.save_image("../images/image1.ppm")
