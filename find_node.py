import cv2
import numpy as np
import os
import sys
import time


def find_node(image: cv2.typing.MatLike, debug=False):
    """
    Normally:
    ---
    Return the a tuple containing the center of the colored node in the
    image. Node color is red.

    When debug enabled, return:
    ---
    1. Tuple of center
    2. Image mask
    3. Contour image
    4. Original image overlaid with center
    """
    tic = time.perf_counter()
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Setting saturation and value numbers to accept wider ranges will
    # mean darker reds are also accepted

    # Masking code generated from ChatGPT

    # Define the lower range for red
    lower_red1 = np.array([0, 55, 55])
    upper_red1 = np.array([10, 255, 255])

    # Define the upper range for red
    lower_red2 = np.array([170, 55, 55])
    upper_red2 = np.array([180, 255, 255])

    # Create masks for both ranges
    mask1 = cv2.inRange(hsv_image, lower_red1, upper_red1)
    mask2 = cv2.inRange(hsv_image, lower_red2, upper_red2)

    # Combine the masks
    red_mask = cv2.bitwise_or(mask1, mask2)

    # Code from below:
    # https://www.geeksforgeeks.org/python-opencv-find-center-of-contour/
    contours, hierarchies = cv2.findContours(
        red_mask, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    
    if debug:
        contour_canvas = np.zeros(red_mask.shape[:2], dtype='uint8')
        cv2.drawContours(contour_canvas, contours, -1, (255, 0, 0), 5)

    overlaid_image = image.copy()

    # Consider the longest contour
    max_contour_len = 0
    longest_contour = None
    for i, c in enumerate(contours):
        # print(f"{i}, length {len(c)}: {c}")
        if len(c) > max_contour_len:
            max_contour_len = len(c)
            longest_contour = c

    M = cv2.moments(longest_contour) # type: ignore
    center_found = False
    if M['m00'] != 0:
        cx = int(M['m10']/M['m00'])
        cy = int(M['m01']/M['m00'])
        center_found = True
        if debug:
            # cv2.drawContours(overlaid_image, [i], -1, (0, 255, 0), 2)
            cv2.circle(overlaid_image, (cx, cy), 10, (255, 0, 0), -1)
            # cv2.putText(overlaid_image, "center", (cx - 20, cy - 20),
            #             cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)
            # print(f"x: {cx} y: {cy}")
    else:
        # This might happen if no node is detected
        print("No red detected", file=sys.stderr)

    center = (cx, cy) if center_found else None
    toc = time.perf_counter()
    print(f"find_node: took {toc-tic: 0.4f} s", file=sys.stderr)

    if debug:
        if center:
            cv2.circle(overlaid_image, center, 15, (0, 255, 0), -1)
        return center, red_mask, contour_canvas, overlaid_image
    return center


# For testing
if __name__ == "__main__":
    input_path = "input/detection_test"
    output_path = "output/detection_test_result"
    for dir_entry in os.scandir(input_path):
        filepath = dir_entry.path
        img = cv2.imread(filepath)

        center, red_mask, contour_canvas, image = find_node(img, True) # type: ignore
        print(f"\"{filepath}\", center is: {center}")
        output_test_dir_path = os.path.join(
            output_path, dir_entry.name.split('.')[0])
        os.makedirs(output_test_dir_path, exist_ok=True)
        
        cv2.imwrite(
            os.path.join(output_test_dir_path, "original_img.jpg"), img)
        cv2.imwrite(
            os.path.join(output_test_dir_path, "red_mask.jpg"), red_mask) # type: ignore
        cv2.imwrite(
            os.path.join(output_test_dir_path, "countour_canvas.jpg"),
            contour_canvas)
        cv2.imwrite(
            os.path.join(output_test_dir_path, "image.jpg"), image)
