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
    prev_time = start_time
    while True:
        curr_time = time.monotonic()
        if (curr_time - prev_time >= data_interval):
            prev_time = curr_time
            timestamp = curr_time - start_time
            ret, frame = vid.read()

            red_nodes = find_node(frame, RED, num_nodes['red'])
            yellow_nodes = find_node(frame, YELLOW, num_nodes['yellow'])
            orange_nodes = find_node(frame, ORANGE, num_nodes['orange'])
            green_nodes = find_node(frame, GREEN, num_nodes['green'])
            blue_nodes = find_node(frame, BLUE, num_nodes['blue'])
            purple_nodes = find_node(frame, PURPLE, num_nodes['purple'])
            pink_nodes = find_node(frame, PINK, num_nodes['pink'])
            black_nodes = find_node(frame, BLACK, num_nodes['black'])

            print(f"t = {timestamp} s")
            print("\t", end="")
            for node in red_nodes:
                cv2.circle(frame, node, 5, BGR_RED, 2, -1)
                print(node, end=" ")
            for node in yellow_nodes:
                cv2.circle(frame, node, 5, BGR_YELLOW, 2, -1)
                print(node, end=" ")
            for node in orange_nodes:
                cv2.circle(frame, node, 5, BGR_ORANGE, 2, -1)
                print(node, end=" ")
            for node in green_nodes:
                cv2.circle(frame, node, 5, BGR_GREEN, 2, -1)
                print(node, end=" ")
            for node in blue_nodes:
                cv2.circle(frame, node, 5, BGR_BLUE, 2, -1)
                print(node, end=" ")
            for node in purple_nodes:
                cv2.circle(frame, node, 5, BGR_PURPLE, 2, -1)
                print(node, end=" ")
            for node in pink_nodes:
                cv2.circle(frame, node, 5, BGR_PINK, 2, -1)
                print(node, end=" ")
            for node in black_nodes:
                cv2.circle(frame, node, 5, BGR_BLACK, 2, -1)
                print(node, end=" ")

            print()
            cv2.imshow('frame', frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    vid.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
