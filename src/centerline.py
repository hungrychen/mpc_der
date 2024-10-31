import cv2
import numpy as np
from skimage import morphology
from skimage.util import invert


def main():
    vid = cv2.VideoCapture(0)

    while True:
        ret, frame = vid.read()
        if not ret:
            exit(1)
        orig = frame.copy()

        # https://www.tutorialspoint.com/opencv-python-how-to-convert-a-colored-image-to-a-binary-image
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        ret, frame = cv2.threshold(frame, 120, 255, 0)
        frame = invert(frame)
        frame = morphology.skeletonize(frame)
        frame = frame.view(dtype=np.uint8)
        frame[frame > 0] = 255
        # print(*frame, sep="\n")

        cv2.imshow("orig", orig)
        cv2.imshow("frame", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    vid.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
