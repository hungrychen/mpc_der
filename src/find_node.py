import cv2
import numpy as np
import heapq
from utils import *


def find_node(
    image: cv2.typing.MatLike, color: int, num_nodes: int, debug: bool = False
) -> list[tuple[int, int]]:
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
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    color_mask = get_mask(hsv_image, color)

    # Consult:
    # https://www.geeksforgeeks.org/python-opencv-find-center-of-contour/

    contours, hierarchies = cv2.findContours(
        color_mask, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE
    )

    contour_len_to_idx = []
    for i, c in enumerate(contours):
        heapq.heappush(contour_len_to_idx, (len(c), i))
    contour_list = []
    if num_nodes > 0:
        contour_list = contour_len_to_idx[-num_nodes:]

    center_list = []
    for c_len, c_idx in contour_list:
        mom = cv2.moments(contours[c_idx])
        if mom["m00"] != 0:
            cx = int(mom["m10"] / mom["m00"])
            cy = int(mom["m01"] / mom["m00"])
            center_list.append((cx, cy))

    return center_list


def get_mask(hsv_image: cv2.typing.MatLike, color: int):
    """
    With the hsv image as input, return the masked image for the color
    indicated
    """
    # Setting saturation and value numbers to accept wider ranges will
    # mean darker colors are also accepted
    # Masking code started with code from ChatGPT

    # The program seems to work best with red, yellow, green
    # Blue, purple do not work as well as they are dark colors

    if color == RED:
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
        color_mask = cv2.bitwise_or(mask1, mask2)
    elif color == YELLOW:
        lower_yellow = np.array([20, 55, 55])
        upper_yellow = np.array([40, 255, 255])

        color_mask = cv2.inRange(hsv_image, lower_yellow, upper_yellow)
    elif color == GREEN:
        lower_green = np.array([50, 55, 55])
        upper_green = np.array([80, 255, 255])

        color_mask = cv2.inRange(hsv_image, lower_green, upper_green)
    elif color == BLUE:
        lower_blue = np.array([105, 45, 45])
        upper_blue = np.array([130, 255, 255])

        color_mask = cv2.inRange(hsv_image, lower_blue, upper_blue)
    elif color == PURPLE:
        lower_purple = np.array([130, 45, 45])
        upper_puple = np.array([150, 255, 255])

        color_mask = cv2.inRange(hsv_image, lower_purple, upper_puple)
    elif color == PINK:
        # Define the lower range for red
        lower_red1 = np.array([0, 20, 55])
        upper_red1 = np.array([10, 255, 255])

        # Define the upper range for red
        lower_red2 = np.array([170, 20, 55])
        upper_red2 = np.array([180, 255, 255])

        # Create masks for both ranges
        mask1 = cv2.inRange(hsv_image, lower_red1, upper_red1)
        mask2 = cv2.inRange(hsv_image, lower_red2, upper_red2)

        # Combine the masks
        color_mask = cv2.bitwise_or(mask1, mask2)

    else:
        raise ValueError("Color not available")

    return color_mask


# For testing
# if __name__ == "__main__":
#     input_path = "input/detection_test"
#     output_path = "output/detection_test_result"
#     for dir_entry in os.scandir(input_path):
#         filepath = dir_entry.path
#         img = cv2.imread(filepath)

#         center, red_mask, contour_canvas, image = find_node(img, GREEN, True) # type: ignore
#         print(f"\"{filepath}\", center is: {center}")
#         output_test_dir_path = os.path.join(
#             output_path, dir_entry.name.split('.')[0])
#         os.makedirs(output_test_dir_path, exist_ok=True)

#         cv2.imwrite(
#             os.path.join(output_test_dir_path, "original_img.jpg"), img)
#         cv2.imwrite(
#             os.path.join(output_test_dir_path, "red_mask.jpg"), red_mask) # type: ignore
#         cv2.imwrite(
#             os.path.join(output_test_dir_path, "countour_canvas.jpg"),
#             contour_canvas
#         )
#         cv2.imwrite(
#             os.path.join(output_test_dir_path, "image.jpg"), image)
