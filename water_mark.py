# import the necessary packages
import argparse
import os

import cv2
import numpy as np
from imutils import paths
from functions import watermarker




# construct the argument parse and parse the arguments
def watermark_maker(watermark_path, input_path, output_path, alpha, posH=0, posW=0):
    watermark = cv2.imread(watermark_path, cv2.IMREAD_UNCHANGED)

    # split the watermark into its respective Blue, Green, Red, and
    # Alpha channels; then take the bitwise AND between all channels
    # and the Alpha channels to construct the actaul watermark
    # NOTE: I'm not sure why we have to do this, but if we don't,
    # pixels are marked as opaque when they shouldn't be

    # loop over the input images
    for imagePath in paths.list_images(input_path):
        # load the input image, then add an extra dimension to the
        # image (i.e., the alpha transparency)
        image = cv2.imread(imagePath)
        print("processing image: ", imagePath)

        # construct an overlay that is the same size as the input
        # image, (using an extra dimension for the alpha transparency),
        # then add the watermark to the overlay in the bottom-right
        # corner
        new_image = watermarker(watermark, image, alpha, posH, posW)
        filename = imagePath[imagePath.rfind(os.path.sep) + 1:]
        p = os.path.sep.join((output_path, filename))
        cv2.imwrite(p, new_image)


ap = argparse.ArgumentParser()
ap.add_argument("-w", "--watermark", required=True,
                help="path to watermark image (assumed to be transparent PNG)")
ap.add_argument("-i", "--input", required=True,
                help="path to the input directory of images")
ap.add_argument("-o", "--output", required=True,
                help="path to the output directory")
ap.add_argument("-a", "--alpha", type=float, default=0.25,
                help="alpha transparency of the overlay (smaller is more transparent)")
args = vars(ap.parse_args())

# load the watermark image, making sure we retain the 4th channel
# which contains the alpha transparency
watermark_path = args["watermark"]
input_path = args["input"]
output_path = args["output"]
alpha = args["alpha"]

watermark_maker(watermark_path, input_path, output_path, alpha, 10, 10)
