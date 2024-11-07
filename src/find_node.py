import cv2
import numpy as np
import heapq
from utils import *


# def find_nodes(
#     image: cv2.typing.MatLike, num_search: dict[int, int], n_nodes: int
# ) -> np.ndarray:
#     """
#     The value (-1, -1) indicates that a node was not found.
#     Returns the positions as a Numpy array of the form
#     [x_1, y_1, x_2, y_2, ..., x_n, y_n], with the colors in the order
#     they were entered
#     """
#     arr = np.empty((1, 2*n_nodes))

#     for color in num_search:
#         pass

#     return arr


def find_node(
    image: cv2.typing.MatLike, color: int, num_nodes: int
) -> list[tuple[int, int]]:
    """
    Return the a tuple containing the center of the colored node in the
    image.
    """
    if num_nodes <= 0:
        return []

    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    color_mask = get_mask(hsv_image, color)

    # Consult:
    # https://www.geeksforgeeks.org/python-opencv-find-center-of-contour/

    contours, hierarchies = cv2.findContours(
        color_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
    )

    contour_len_to_idx = []
    for i, c in enumerate(contours):
        heapq.heappush(contour_len_to_idx, (len(c), i))

    center_list = []
    for c_len, c_idx in contour_len_to_idx:
        mom = cv2.moments(contours[c_idx])
        if mom["m00"] != 0:
            cx = int(mom["m10"] / mom["m00"])
            cy = int(mom["m01"] / mom["m00"])
            point = (cx, cy)
            if not exists_point_within_dist(
                point, center_list, MIN_NODE_SEPARATION
            ):
                center_list.append(point)
                if len(center_list) == num_nodes:
                    break

    return center_list


def exists_point_within_dist(test_point, collection_of_points, dist):
    test_point_t = np.array(test_point)
    for collection_point in collection_of_points:
        if np.linalg.norm(test_point_t - np.array(collection_point)) < dist:
            return True
    return False


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
    elif color == ORANGE:
        lower_orange = np.array([10, 55, 55])
        upper_orange = np.array([30, 255, 255])

        color_mask = cv2.inRange(hsv_image, lower_orange, upper_orange)
    elif color == GREEN:
        lower_green = np.array([50, 55, 55])
        upper_green = np.array([80, 255, 255])

        color_mask = cv2.inRange(hsv_image, lower_green, upper_green)
    elif color == BLUE:
        lower_blue = np.array([105, 45, 45])
        upper_blue = np.array([115, 255, 255])

        color_mask = cv2.inRange(hsv_image, lower_blue, upper_blue)
    elif color == PURPLE:
        lower_purple = np.array([120, 40, 40])
        upper_puple = np.array([150, 255, 255])

        color_mask = cv2.inRange(hsv_image, lower_purple, upper_puple)
    elif color == PINK:
        # Define the lower range for red
        lower_pink1 = np.array([0, 20, 55])
        upper_pink1 = np.array([10, 255, 255])

        # Define the upper range for red
        lower_pink2 = np.array([170, 20, 55])
        upper_pink2 = np.array([180, 255, 255])

        # Create masks for both ranges
        mask1 = cv2.inRange(hsv_image, lower_pink1, upper_pink1)
        mask2 = cv2.inRange(hsv_image, lower_pink2, upper_pink2)

        # Combine the masks
        color_mask = cv2.bitwise_or(mask1, mask2)
    elif color == BLACK:
        lower_black = np.array([0, 0, 0])
        upper_black = np.array([255, 255, 40])

        color_mask = cv2.inRange(hsv_image, lower_black, upper_black)
    else:
        raise ValueError("Color not available")

    return color_mask
