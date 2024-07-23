import cv2
import numpy as np


def find_node(image, debug=False):
    """
    Return the center of the colored node in the image. Node color is
    red.

    When debug is True, return the image with the node point
    highlighted.
    """
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Define the lower range for red
    lower_red1 = np.array([0, 100, 100])
    upper_red1 = np.array([10, 255, 255])

    # Define the upper range for red
    lower_red2 = np.array([170, 100, 100])
    upper_red2 = np.array([180, 255, 255])

    # Create masks for both ranges
    mask1 = cv2.inRange(hsv_image, lower_red1, upper_red1)
    mask2 = cv2.inRange(hsv_image, lower_red2, upper_red2)

    # Combine the masks
    red_mask = cv2.bitwise_or(mask1, mask2)
    non_zero = np.argwhere(red_mask != 0)
    print(non_zero)
    center = np.median(non_zero, axis=0)

    if not debug:
        return center
    
    import matplotlib.pyplot as plt
    
    rev_center = []
    for item in reversed(center):
        rev_center.append(int(item))
    image_with_node = cv2.putText(image, "x",
                                  rev_center, cv2.FONT_HERSHEY_SIMPLEX,
                                  10, (0,0,0), 20)
    image_with_node = cv2.putText(image, "*",
                                  (non_zero[0,1], non_zero[0,0]), cv2.FONT_HERSHEY_SIMPLEX,
                                  10, (0,0,0), 20)
    image_with_node = cv2.putText(image, "*",
                                  (non_zero[-1,1], non_zero[-1,0]), cv2.FONT_HERSHEY_SIMPLEX,
                                  10, (0,0,0), 20)

    red_mask = cv2.putText(red_mask, "x",
                           rev_center, cv2.FONT_HERSHEY_SIMPLEX,
                           10, (255,0,0), 20)
    
    # plt.scatter(-non_zero[:,0], -non_zero[:,1])
    # plt.show()

    return center, image_with_node, red_mask
    

# For testing
if __name__ == "__main__":
    img = cv2.imread("test.jpg")

    center, img_out, mask_img = find_node(img, True)
    print(center)
    cv2.imshow("img_out", img_out)
    cv2.waitKey(0)
    cv2.imshow("mask_img", mask_img)
    cv2.waitKey(0)
