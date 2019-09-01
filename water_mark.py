# import the necessary packages
import argparse
import os

import cv2
import numpy as np
from imutils import paths

def watermarker(watermark, image, alpha,posH, posW):
    (wH, wW) = watermark.shape[:2]
    (B, G, R, A) = cv2.split(watermark)
    B = cv2.bitwise_and(B, B, mask=A)
    G = cv2.bitwise_and(G, G, mask=A)
    R = cv2.bitwise_and(R, R, mask=A)
    watermark = cv2.merge([B, G, R, A])
    # (h, w) = image.shape[:2]
    # watermark_new = watermark.copy()
    # if image.mean() < 100:
    #     watermark_new[0: wH, 0:wW, 0:3] = 255 - watermark_new[0: wH, 0:wW, 0: 3]
    #     print("changed")
    # image = np.dstack([image, np.ones((h, w), dtype="uint8") * 255])
    # overlay = np.zeros((h, w, 4), dtype="uint8")
    # overlay[posH: wH + posH, posW: wW + posW] = watermark_new
    # alpha_255 = alpha * 255
    # alpha_255 = np.dtype(np.uint8).type(alpha_255)
    #
    # c = image[overlay[:, :, 3] == 255]
    # c = c.astype(float)
    # c *= (1 - alpha)
    # c = c.astype(np.uint8)
    # image[overlay[:, :, 3] == 255] = c
    # # print(image[overlay[:, :, 3] == 255])
    # d = image[overlay[:, :, 3] == 255]
    # d = d.astype(float)
    # d *= alpha
    # d = d.astype(float)
    # overlay[overlay[:, :, 3] == 255] = d
    # overlay[overlay[:, :, 3] == 0] = [0, 0, 0, 255]
    # new_image = cv2.add(image, overlay)

    (h, w) = image.shape[:2]
    watermark_new = watermark.copy()
    if image.mean() < 100:
        watermark_new[0: wH, 0:wW, 0:3] = 255 - watermark_new[0: wH, 0:wW, 0: 3]
        print("changed")
    image = np.dstack([image, np.ones((h, w), dtype="uint8") * 255])

    # construct an overlay that is the same size as the input
    # image, (using an extra dimension for the alpha transparency),
    # then add the watermark to the overlay in the bottom-right
    # corner
    overlay = np.zeros((h, w, 4), dtype="uint8")
    overlay[posH: wH + posH, posW: posW + 10] = watermark_new
    new_image = np.zeros((h, w, 4), dtype="uint8")
    row_number = 0
    while row_number < wH + 10:
        column_number = 0
        while column_number < wW + 10:
            if (overlay[row_number][column_number][3]) < 0.5:
                i += 1
                new_image[row_number][column_number] = image[row_number][column_number]
            else:
                cv2.addWeighted(image[row_number][column_number], 1 - alpha,
                                overlay[row_number][column_number],
                                alpha, 0, new_image[row_number][column_number])
            column_number += 1
        row_number += 1
    new_image[row_number:h, 0: w] = image[row_number:h, 0: w]
    new_image[0: row_number, column_number: w] = image[0: row_number, column_number: w]

    return new_image




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
