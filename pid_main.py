import simple_pid
import selectors
import sys
import cv2
import numpy as np
from motor_connection import Motor
from find_node import find_node
from utils import *
import time


INIT_POS = 0.5
K_P = .04
K_I = .004
K_D = .001
EDGE_CORRECTION_CTRL = .003

def main():
    config = read_config()

    vid = cv2.VideoCapture(0)
    motor = Motor(config["motor_ids"][0],
                  config["port"],
                  config["baudrate"],
                  def_speed=config["motor_speeds"][0])
    sel = selectors.DefaultSelector()
    sel.register(sys.stdin, selectors.EVENT_READ)
    
    motor.custom_move(INIT_POS)
    while True:
        pos = motor.get_pos()
        if pos > INIT_POS-.05 and pos < INIT_POS+.05:
            break
    pid_controller = simple_pid.PID(K_P, K_I, K_D, setpoint=INIT_POS)

    show_video = config["show_video"]
    if show_video:
        ret, frame = vid.read()
        cv2.imshow('frame', frame)
        cv2.waitKey(1)
    else:
        print("Modify config.json to show video", file=sys.stderr)

    prev_node_center = None
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
                pid_controller.reset()
                pid_controller.setpoint = clip(num, 0., 1.)
        
        ret, frame = vid.read()
        node_center_list = find_node(frame, RED, 1)
        node_center = None

        if node_center_list:
            node_center = node_center_list[0]
            cx, cy = node_center
            norm_cy = cy / FRAME_Y_MAX
            prev_node_center = node_center
            control = pid_controller(norm_cy)
        elif prev_node_center:
            cx, cy = prev_node_center
            norm_cy = cy / FRAME_Y_MAX
            if norm_cy > 0.5:
                control = -EDGE_CORRECTION_CTRL
            elif norm_cy <= 0.5:
                control = EDGE_CORRECTION_CTRL
            pid_controller.reset()

        # print(f"{norm_cy: 0.4f}, {control: 0.4f}")
        motor.adjust_move(control)

        if show_video:
            if node_center is not None:
                cv2.circle(frame, node_center, 5, (0, 0, 255), 2, -1)
            setpoint = pid_controller.setpoint
            setpoint_y_coord = int(setpoint*FRAME_Y_MAX)
            cv2.putText(frame, f"SETPOINT: {setpoint}",
                        (10, setpoint_y_coord - 4),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (50, 50, 255))
            frame = cv2.line(frame,
                             (FRAME_X_MIN, setpoint_y_coord),
                             (FRAME_X_MAX, setpoint_y_coord),
                             (255, 255, 255))
            cv2.imshow('frame', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    vid.release()
    cv2.destroyAllWindows()
    sel.close()


if __name__ == "__main__":
    main()
