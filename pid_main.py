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
    config = read_config()

    vid = cv2.VideoCapture(0)
    motor = Motor(config["motor_ids"][0],
                  config["port"],
                  config["baudrate"],
                  def_speed=config["motor_speeds"][0])
    sel = selectors.DefaultSelector()
    sel.register(sys.stdin, selectors.EVENT_READ)
    pid_controller = simple_pid.PID(0.03, 0, 0, setpoint=0.5)
    
    motor.custom_move(INIT_POS)
    time.sleep(3)

    show_video = config["show_video"]
    if show_video:
        ret, frame = vid.read()
        cv2.imshow('frame', frame)
        cv2.waitKey(1)
    else:
        print("Modify config.json to show video")

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
                if num < 0.:
                    num = 0.
                elif num > 1.:
                    num = 1.
                pid_controller.setpoint = num
        
        ret, frame = vid.read()
        node_center_list = find_node(frame, RED, 1)
        node_center = None
        if node_center_list:
            node_center = node_center_list[0]

            cx, cy = node_center
            norm_cy = cy / FRAME_Y_MAX
            control = pid_controller(norm_cy)
            # print(f"control: {control}")
            motor.adjust_move(control)

        if show_video:
            if node_center is not None:
                cv2.circle(frame, node_center, 5, (0, 0, 255), 2, -1)
            cv2.putText(frame, f"SETPOINT: {pid_controller.setpoint}", (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (50, 50, 255))
            cv2.imshow('frame', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    vid.release()
    cv2.destroyAllWindows()
    sel.close()


if __name__ == "__main__":
    main()
