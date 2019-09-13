import cv2
import numpy as np

image = cv2.imread("desk.jpg", cv2.IMREAD_UNCHANGED)
(w, h) = image.shape[:2]
print(np.mean(image[0:50, 0:300]))
max_pix = np.max(image)
diff = max_pix - 230
image[image > 230] -= diff
print(np.mean(image[0:50, 0:300]))
cv2.imwrite("desk1.jpg", image)
image = np.dstack([image, np.ones((w, h), dtype="uint8") * 255])











# border = cv2.imread("google.png", cv2.IMREAD_UNCHANGED)
# border_resized = cv2.resize(border, (h, w), interpolation=cv2.INTER_LINEAR)
# print(border_resized.shape)
# print(border_resized[0, 0])
# print(border_resized[600, 600])
# # print(border_resized[:,:,3] == 0)
# border_resized[0, 0] = [0,0,0,255]
# image[border_resized[:, :, 3] == 255] = [0, 0, 0, 255]
# border_resized[border_resized[:, :, 3] == 0] = [0, 0, 0, 255]
# print(border_resized[0, 0])
# print(border_resized[600, 600])
# output = cv2.add(border_resized, image)
# cv2.imshow("output", output)
# cv2.waitKey(0)

