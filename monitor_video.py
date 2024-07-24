# Acknowledgements: 
# https://www.geeksforgeeks.org/python-opencv-capture-video-from-camera/

import cv2
from find_node import find_node
from utils import *


def main():
    # define a video capture object
    vid = cv2.VideoCapture(0)
    
    while True: 
        # Capture the video frame by frame 
        ret, frame = vid.read()
    
        # Display the resulting frame
        red_node = find_node(frame, RED)
        yellow_node = find_node(frame, YELLOW)
        green_node = find_node(frame, GREEN)
        if red_node:
            cv2.circle(frame, red_node, 5, (0, 0, 255), 5, -1)
        if yellow_node:
            cv2.circle(frame, yellow_node, 5, (0, 255, 255), 5, -1)
        if green_node:
            cv2.circle(frame, green_node, 5, (0, 255, 0), 5, -1)
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
