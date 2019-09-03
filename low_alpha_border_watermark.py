import argparse
import os
import cv2
import numpy as np
from imutils import paths
from functions import *
import tinify

parser = argparse.ArgumentParser()
parser.add_argument("-w", "--watermark", required=True,
                    help="path to watermark image (assumed to be transparent PNG)")
parser.add_argument("-i", "--input", required=True,
                    help="path to the input directory of images")
parser.add_argument("-o", "--output", required=True,
                    help="path to the output directory")
parser.add_argument("-wa", "--watermarkalpha", type=float, default=0.25,
                    help="alpha transparency of watermark between 0.0 and 1.0 (smaller is more transparent)")
parser.add_argument("-ba", "--borderalpha", type=float, default=0.5,
                    help="alpha transparency of border between 0.0 and 1.0 (smaller is more transparent)")
parser.add_argument("-g", "--greyness", type = float, default=1.0,
                    help="greyness of border between 0.0 and 1.0 (smaller is darker)")
parser.add_argument("-br", "--borderratio", type=float, default=0.05,
                    help="ratio of border to picture size")
parser.add_argument("-wr", "--watermarkratio", type=float, default=0.01,
                    help="ratio of space between watermark and border to picture size")
parser.add_argument("-s", "--size", type=float, default=0.2,
                    help="ratio of size of watermark to image size")
parser.add_argument("-c", "--compress", type=bool, default=False,
                    help="compress or not")
parser.add_argument("-k", "--key", type=str, default="kkkjgRvpZ75MJ470Fn9Cxfr5MG59ShdM",
                    help="tinify register key")
arg = vars(parser.parse_args())


watermark_path = arg["watermark"]
input_path = arg["input"]
output_path = arg["output"]
watermark_alpha = arg["watermarkalpha"]
border_alpha = arg["borderalpha"]
greyness = arg["greyness"]
border_ratio = arg["borderratio"]
watermark_ratio = arg["watermarkratio"]
watermark_size = arg["size"]
is_compress = arg["compress"]
key = arg["key"]

watermark = cv2.imread(watermark_path, cv2.IMREAD_UNCHANGED)
(wH, wW) = watermark.shape[:2]
if is_compress:
    set_tinify_key(key)
print(watermark.shape)
for imagePath in paths.list_images(input_path):
    # load the input image, then add an extra dimension to the
    # image (i.e., the alpha transparency)
    image = cv2.imread(imagePath)
    (h, w) = image.shape[:2]
    posH = int(h * (border_ratio + watermark_ratio))
    posW = int(w * (border_ratio + watermark_ratio))
    watermark_h = int(watermark_size * h)
    watermark_w = int(wW * watermark_h / wH)
    watermark_resized = cv2.resize(watermark, (watermark_w, watermark_h), interpolation=cv2.INTER_LINEAR)
    print("processing image: ", imagePath)
    bordered_image = low_opacity_borderer(image, percent=border_ratio, alpha=border_alpha, greyness=greyness)
    # construct an overlay that is the same size as the input
    # image, (using an extra dimension for the alpha transparency),
    # then add the watermark to the overlay in the bottom-right
    # corner
    new_image = watermarker(watermark_resized, bordered_image, watermark_alpha, posH, posW)
    filename = imagePath[imagePath.rfind(os.path.sep) + 1:]
    p = os.path.sep.join((output_path, filename))
    cv2.imwrite(p, new_image)
    if is_compress:
        image = compressor(p)
        image.to_file(p)
