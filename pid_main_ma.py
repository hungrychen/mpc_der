import simple_pid
import selectors
import sys
import cv2
import numpy as np
from collections import deque
from motor_connection import Motor
from find_node import find_node
from utils import *
import time


INIT_POS = (0.5, 0.5)

# Mean tuning
# K_P = .08
# K_I = .004
# K_D = .005

# PTP tuning
K_P = .06
K_I = .004
K_D = .02

# Autotuned
# K_P = 0.02061
# K_I = 0.003472
# K_D = 0.0
OUTPUT_LIMITS = (-0.3, 0.3)

# LPF_ALPHA = 0.07

EDGE_CORRECTION_CTRL = .003

# Mean tuning
# MA_WINDOW = 15

# PTP tuning
MA_WINDOW = 12

def main():
    config = read_config()

    vid = cv2.VideoCapture(0)
    motor = Motor(config["motor_ids"][0],
                  config["port"],
                  config["baudrate"],
                  def_speed=config["motor_speeds"][0])
    sel = selectors.DefaultSelector()
    sel.register(sys.stdin, selectors.EVENT_READ)
    
    motor.custom_move(INIT_POS[1], block=True)
    # time.sleep(2)
    pid_controller = simple_pid.PID(K_P, K_I, K_D, setpoint=INIT_POS[1],
                                    output_limits=OUTPUT_LIMITS,)

    show_video = config["show_video"]
    if show_video:
        ret, frame = vid.read()
        cv2.imshow('frame', frame)
        cv2.waitKey(1)
    else:
        print("Modify config.json to show video", file=sys.stderr)

    node_center_list = None
    while not node_center_list:
        node_center_list = find_node(frame, RED, 1)
        print("Place node in camera frame")
    # cx, cy = node_center_list[0]
    node_center = node_center_list[0]

    node_center_hist = np.empty((MA_WINDOW, 2))
    node_center_hist[:,:] = node_center
    print(node_center_hist)
    # node_center_hist[:,0] = INIT_POS[0] * FRAME_X_MAX
    # node_center_hist[:,1] = INIT_POS[1] * FRAME_Y_MAX

    ctrl_pos = np.array(node_center)

    time_start = time.monotonic()
    f = open("output/pid_ptp/data.txt", "w")
    print("time,control,ptp_x,ptp_y", flush=True, file=f)
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

        node_center_hist[:-1,:] = node_center_hist[1:,:]
        if node_center_list:
            node_center = node_center_list[0]

            node_center_hist[-1,0] = node_center[0]
            node_center_hist[-1,1] = node_center[1]

            # mean_pos = np.mean(node_center_hist, axis=0)
            # norm_cy = cy / FRAME_Y_MAX
            # prev_node_center = node_center

        #     norm_mean_cy = mean_pos[1] / FRAME_Y_MAX
        #     control = pid_controller(norm_mean_cy)
        # else:
        #     cx, cy = node_center_hist[-1,:]
        #     norm_cy = cy / FRAME_Y_MAX
        #     if norm_cy > 0.5:
        #         control = -EDGE_CORRECTION_CTRL
        #     else: # norm_cy <= 0.5
        #         control = EDGE_CORRECTION_CTRL
        #     pid_controller.reset()
        
        # mean_pos = np.mean(node_center_hist, axis=0)
        ctrl_pos = np.min(node_center_hist, axis=0) + np.ptp(node_center_hist, axis=0)/2
        # ctrl_pos = LPF_ALPHA * node_center_hist[-1,:] + (1-LPF_ALPHA) * ctrl_pos

        if node_center_list:
            norm_mean_cy = ctrl_pos[1] / FRAME_Y_MAX
            control = pid_controller(norm_mean_cy)
        else:
            cx, cy = node_center_hist[-1,:]
            norm_cy = cy / FRAME_Y_MAX
            if norm_cy > 0.5:
                control = -EDGE_CORRECTION_CTRL
            else: # norm_cy <= 0.5
                control = EDGE_CORRECTION_CTRL
            pid_controller.reset()

        motor.adjust_move(control)
        print(f"{time.monotonic()-time_start: 0.4f},{control: 0.4f},{ctrl_pos[0]: 0.1f},{ctrl_pos[1]: 0.1f}", file=f)
        # print(control)

        if show_video:
            if node_center is not None:
                cv2.circle(frame, node_center, 5, (0, 0, 255), 2, -1)
            cv2.circle(frame, ctrl_pos.astype(int), 2, (255, 0, 0), 1, -1)
            setpoint = pid_controller.setpoint
            setpoint_y_coord = int(setpoint*FRAME_Y_MAX)
            cv2.putText(frame, f"SETPOINT: {setpoint}",
                        (10, setpoint_y_coord - 4),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (50, 50, 255))
            cv2.line(frame,
                     (FRAME_X_MIN, setpoint_y_coord),
                     (FRAME_X_MAX, setpoint_y_coord),
                     (255, 255, 255))
            cv2.imshow('frame', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    vid.release()
    cv2.destroyAllWindows()
    sel.close()
    f.close()


if __name__ == "__main__":
    main()
