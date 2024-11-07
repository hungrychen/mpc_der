#!/usr/bin/env python
"""
For manual calibration:
    ./calibrate.py -m [n_pairs]
For auto calibration:
    ./calibrate.py -a [node_color_code]
"""


import cv2
import numpy as np
from numpy.linalg import norm
from sys import stderr
import argparse
from utils import *
from find_node import find_node


p = argparse.ArgumentParser()
mode = p.add_mutually_exclusive_group(required=True)
mode.add_argument("--manual", "-m", dest="n_pairs", type=int)
mode.add_argument("--auto", "-a", dest="node_color_code", type=int)
args = p.parse_args()

coord = None
auto_cal = args.node_color_code is not None
num_dist = args.n_pairs
dist_count = 0


def get_coord(event, x, y, flags, userdata):
    global coord, dist_count
    if event == cv2.EVENT_LBUTTONDOWN:
        if coord is None:
            coord = np.array((x, y))
            print(coord, file=stderr)
        else:
            last_coord = coord
            coord = np.array((x, y))
            dist = norm(last_coord - coord)
            print(coord, file=stderr)
            print(f"dist: {dist} px", file=stderr)
            print(dist)
            coord = None
            dist_count += 1
            if dist_count == num_dist:
                vid.release()
                cv2.destroyAllWindows()
                exit(0)


cv2.namedWindow(WINNAME)
vid = cv2.VideoCapture(0)
vid.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_Y_MAX)
vid.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_X_MAX)
if auto_cal:
    ret, frame = vid.read()
    cal_nodes = find_node(frame, args.node_color_code, CALIBRATION_NUM_NODES)
    if len(cal_nodes) != CALIBRATION_NUM_NODES:
        raise RuntimeError(
            f"Cannot detect indicated number of nodes {CALIBRATION_NUM_NODES}"
        )
    for node in cal_nodes:
        cv2.circle(frame, node, 5, COLOR_MAP[args.node_color_code], 2, -1)
    print("Press 'c' to confirm calibration, or 'q' to quit", file=stderr)
    while True:
        cv2.imshow(WINNAME, frame)
        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            break
        elif key == ord("c"):
            dist = norm(np.array(cal_nodes[0]) - np.array(cal_nodes[1]))
            print(f"dist: {dist} px", file=stderr)
            print(dist)
            vid.release()
            cv2.destroyAllWindows()
            exit(0)
else:
    cv2.setMouseCallback(WINNAME, get_coord)
    while True:
        ret, frame = vid.read()
        cv2.imshow(WINNAME, frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

vid.release()
cv2.destroyAllWindows()
exit(1)
