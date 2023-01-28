import numpy as np


class Image:

    def __init__(self, width, height):
        # setting image width and height and creating an empty list for the image
        self.width = width
        self.height = height

        self.image_list = np.empty((height, width, 3), dtype=int)

    def save_image(self, path):
        with open(path, "w") as f:
            # write header
            f.write("P3\n")
            f.write(f"{self.width} {self.height} 255\n")
            # write pixels
            for y in range(self.height)[::-1]:
                for x in range(self.width):
                    f.write(f" {self.image_list[y, x, 0]} ")
                    f.write(f" {self.image_list[y, x, 1]} ")
                    f.write(f" {self.image_list[y, x, 2]} ")
