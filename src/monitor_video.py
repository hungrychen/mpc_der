# Acknowledgements: 
# https://www.geeksforgeeks.org/python-opencv-capture-video-from-camera/

import time
import cv2
from find_node import find_node
from utils import *


def main():
    start_time = time.monotonic()
    num_nodes = read_config("./config/config_collect_data.json")['num_nodes']
    print(num_nodes)

    # define a video capture object
    vid = cv2.VideoCapture(0)
    
    while True: 
        # Capture the video frame by frame 
        ret, frame = vid.read()

        # Display the resulting frame
        red_nodes = find_node(frame, RED, num_nodes['red'])
        yellow_nodes = find_node(frame, YELLOW, num_nodes['yellow'])
        green_nodes = find_node(frame, GREEN, num_nodes['green'])
        blue_nodes = find_node(frame, BLUE, num_nodes['blue'])
        purple_nodes = find_node(frame, PURPLE, num_nodes['purple'])
        pink_nodes = find_node(frame, PINK, num_nodes['pink'])
        # black_nodes = find_node(frame, BLACK, num_nodes['black'])

        curr_time = time.monotonic() - start_time
        print(f"t = {curr_time} s")
        print("\t", end="")
        for node in red_nodes:
            cv2.circle(frame, node, 5, (0, 0, 255), 2, -1)
            print(node, end=" ")
        for node in yellow_nodes:
            cv2.circle(frame, node, 5, (0, 255, 255), 2, -1)
            print(node, end=" ")
        for node in green_nodes:
            cv2.circle(frame, node, 5, (0, 255, 0), 2, -1)
            print(node, end=" ")
        for node in blue_nodes:
            cv2.circle(frame, node, 5, (255, 0, 0), 2, -1)
            print(node, end=" ")
        for node in purple_nodes:
            cv2.circle(frame, node, 5, (255, 0, 255), 2, -1)
            print(node, end=" ")
        for node in pink_nodes:
            cv2.circle(frame, node, 5, (50, 50, 255), 2, -1)
            print(node, end=" ")
        # for node in black_nodes:
        #     cv2.circle(frame, node, 5, (0, 0, 0), 2, -1)
        #     print(node, end=" ")

        print()
        cv2.imshow('frame', frame)

        # Press 'q' to quit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # After the loop release the cap object
    vid.release()
    # Destroy all the windows
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
