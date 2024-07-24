import simple_pid
import selectors
import sys
import cv2
from motor_connection import Motor
from find_node import find_node
from utils import *
import time


INIT_POS = 0.5

def main():
    vid = cv2.VideoCapture(0)
    motor = Motor(1, "/dev/ttyUSB0", 1000000, def_speed=512)
    sel = selectors.DefaultSelector()
    sel.register(sys.stdin, selectors.EVENT_READ)
    pid_controller = simple_pid.PID(0.07, 0, 0, setpoint=0.5)
    
    motor.custom_move(INIT_POS)
    time.sleep(1)

    ret, frame = vid.read()
    cv2.imshow('frame', frame)
    cv2.waitKey(1)

    while True:
        if sel.select(0):
            text = input()

            if text == "q":
                break

            try:
                num = float(text)
            except:
                print("Must enter number", file=sys.stderr)
            else:
                pid_controller.setpoint = num
        
        ret, frame = vid.read()
        node_center = find_node(frame)
        if node_center:
            if len(sys.argv) == 2 and sys.argv[1] == "-v":
                cv2.circle(frame, node_center, 5, (255, 0, 0), 20, -1)
                cv2.imshow('frame', frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

            cx, cy = node_center
            norm_cy = cy / FRAME_Y_MAX
            control = pid_controller(norm_cy)
            # print(f"control: {control}")
            motor.adjust_move(control)

    vid.release()
    cv2.destroyAllWindows()
    sel.close()


if __name__ == "__main__":
    main()
