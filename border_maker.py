import argparse
import os

import cv2
import numpy as np
from imutils import paths

def borderer(border, image):
    print(border.shape)
    (w, h) = image.shape[:2]
    image = np.dstack([image, np.ones((w, h), dtype="uint8") * 255])
    border_resized = cv2.resize(border, (h, w))
    print(border_resized.shape)
    image[border_resized[:, :, 3] == 255] = [0, 0, 0, 255]
    border_resized[border_resized[:, :, 3] == 0] = [0, 0, 0, 255]
    return cv2.add(image, border_resized)

def border_maker(border_path, input_path, output_path):
    border = cv2.imread(border_path, cv2.IMREAD_UNCHANGED)
    print(border.shape)
    for image_path in paths.list_images(input_path):
        image = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
        print("bordering image: ", image_path)
        output = borderer(border, image)
        filename = image_path[image_path.rfind(os.path.sep) + 1:]
        p = os.path.sep.join((output_path, filename))
        cv2.imwrite(p, output)


ap = argparse.ArgumentParser()
ap.add_argument("-b", "--border", required=True,
                help="path to border image (assumed to be transparent PNG)")
ap.add_argument("-i", "--input", required=True,
                help="path to the input directory of images")
ap.add_argument("-o", "--output", required=True,
                help="path to the output directory")
args = vars(ap.parse_args())

border_path = args["border"]
input_path = args["input"]
output_path = args["output"]

border_maker(border_path, input_path, output_path)
