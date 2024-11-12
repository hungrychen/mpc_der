import cv2
from find_node import find_node
from utils import *


def get_top_node(config_file: str):
    config = read_config(config_file)

    vid = cv2.VideoCapture(0)
    vid.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_Y_MAX)
    vid.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_X_MAX)

    ret, frame = vid.read()
    nodes = find_node(
        frame,
        DEF_EXPERIMENT_COLOR,
        config["num_nodes"][DEF_EXPERIMENT_COLOR_STR],
    )

    top_node = min(nodes, key=lambda coord: coord[1])
    print("Press 'c' to confirm or 'q' to recalibrate")
    success = False
    while True:
        cv2.circle(frame, top_node, 5, COLOR_MAP[DEF_EXPERIMENT_COLOR], 2, -1)
        cv2.imshow(WINNAME, frame)
        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            break
        elif key == ord("c"):
            success = True
            break

    vid.release()
    cv2.destroyAllWindows()
    return success, top_node
