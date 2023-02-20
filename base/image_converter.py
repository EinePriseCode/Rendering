import cv2
import os

in_dir = "../images/"
ex_dir = "../images_report/"

file_names = os.listdir(in_dir)

for file_name in file_names:
    file_split = file_name.split(".")
    if file_split[1] == "ppm":
        img = cv2.imread(in_dir + file_name)
        cv2.imwrite(ex_dir + file_split[0] + ".png", img)

        print("Converted and saved in " + ex_dir + file_split[0] + ".png!")

