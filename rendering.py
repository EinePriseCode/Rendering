import numpy as np

from camera import Camera


class Image:

    def __init__(self, width, height):
        # setting image width and height and creating an empty list for the image
        self.width = width
        self.height = height

        self.image_list = np.empty((height, width, 3), dtype=int)

    def render(self):
        # looping through pixels for rendering

        c = Camera(0.0035, 16 / 9, 100)

        for y in range(self.height):
            for x in range(self.width):
                ray = c.get_ray(x, y)
                self.image_list[y, x] = c.ray_color(ray)

    def save_image(self, path):
        with open(path, "w") as f:
            # write header
            f.write("P3\n")
            f.write(f"{self.width} {self.height} 255\n")
            # write pixels
            for y in range(self.height):
                for x in range(self.width):
                    f.write(f" {self.image_list[y, x, 0]} ")
                    f.write(f" {self.image_list[y, x, 1]} ")
                    f.write(f" {self.image_list[y, x, 2]} ")


i = Image(1920, 1080)
i.render()
i.save_image("rendering2.ppm")