import cv2

image = cv2.imread("input/11308-8.jpg", cv2.IMREAD_UNCHANGED)
print(image.mean())

