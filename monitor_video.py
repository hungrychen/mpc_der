# Acknowledgements: 
# https://www.geeksforgeeks.org/python-opencv-capture-video-from-camera/

import cv2
from find_node import find_node


def main():
    # define a video capture object
    vid = cv2.VideoCapture(0)
    
    while True: 
        # Capture the video frame by frame 
        ret, frame = vid.read()
    
        # Display the resulting frame
        node = find_node(frame)
        if node:
            cv2.circle(frame, node, 5, (255, 0, 0), 20, -1) # type: ignore
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
