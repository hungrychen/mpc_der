# Acknowledgements: 
# https://www.geeksforgeeks.org/python-opencv-capture-video-from-camera/

import cv2
from find_node import find_node
from utils import *


def main():
    num_nodes = read_config()['num_nodes']
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
        for node in red_nodes:
            cv2.circle(frame, node, 5, (0, 0, 255), 5, -1)
        for node in yellow_nodes:
            cv2.circle(frame, node, 5, (0, 255, 255), 5, -1)
        for node in green_nodes:
            cv2.circle(frame, node, 5, (0, 255, 0), 5, -1)
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
