# Acknowledgements: 
# https://www.geeksforgeeks.org/python-opencv-capture-video-from-camera/


import time
import cv2
from find_node import find_node
from utils import *


def main():
    config = read_config("./config/config_collect_data.json")
    data_interval = config["data_interval"]
    num_nodes = config['num_nodes']
    print(num_nodes)

    vid = cv2.VideoCapture(0)
    vid.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_Y_MAX)
    vid.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_X_MAX)

    start_time = time.monotonic()
    while True:
        ret, frame = vid.read()
        curr_time = time.monotonic() - start_time
        print(f"t={curr_time}")
        cv2.imshow('frame', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    vid.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
