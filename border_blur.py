import cv2
import numpy as np
from functions import low_opacity_borderer,blurer


image = cv2.imread("1066-666.jpg")
new_image = low_opacity_borderer(image, 0.05, 0.5, 0.5)
cv2.imwrite("test.png", new_image)
new_image = blurer(image, 0.05, (50, 50))
print(new_image.shape)
cv2.imwrite("test2.png", new_image)
