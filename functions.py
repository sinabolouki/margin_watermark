import cv2
import numpy as np

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
    print(posH)
    overlay[posH: wH + posH, posW: wW + posW] = watermark_new
    new_image = np.zeros((h, w, 4), dtype="uint8")
    row_number = 0
    while row_number < wH + posH:
        column_number = 0
        while column_number < wW + posW:
            if (overlay[row_number][column_number][3]) < 0.5:
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

def low_opacity_borderer(image, percent, alpha, greyness=1.0):
    greyness_255 = greyness * 255
    greyness_255 = np.dtype(np.uint8).type(greyness_255)
    border_color = [greyness_255, greyness_255, greyness_255]
    alpha_255 = alpha * 255
    alpha_255 = np.dtype(np.uint8).type(alpha_255)
    (h, w) = image.shape[:2]
    start_height = int(h * percent)
    end_height = h - start_height
    start_width = int(w * percent)
    end_width = w - start_width
    black_image = np.zeros((h, w, 3), dtype=np.uint8)
    black_image[:start_height + 1, :] = border_color
    black_image[:, :start_width + 1, :] = border_color
    black_image[end_height:, :] = border_color
    black_image[:, end_width:] = border_color
    image_new = cv2.addWeighted(black_image, alpha, image, 1, 0)

    return image_new


def blurer(image, percent, kernel_size=(5, 5)):
    (h, w) = image.shape[:2]
    start_height = int(h * percent)
    end_height = h - start_height
    start_width = int(w * percent)
    end_width = w - start_width
    black_image = np.zeros((h, w, 3), dtype=np.uint8)
    black_image[start_height: end_height + 1, start_width: end_width + 1] = \
        image[start_height: end_height + 1, start_width: end_width + 1]
    new_image = cv2.blur(image, kernel_size)
    black_image[:start_height + 1, :] = new_image[:start_height + 1, :]
    black_image[:, :start_width + 1, :] = new_image[:, :start_width + 1, :]
    black_image[end_height:, :] = new_image[end_height:, :]
    black_image[:, end_width:] = new_image[:, end_width:]
    return black_image
