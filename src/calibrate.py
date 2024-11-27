import cv2
import numpy as np
from numpy.linalg import norm
from sys import stderr
import os
import argparse
from utils import *
from find_node import find_node


def get_coord(event, x, y, flags, userdata):
    if event == cv2.EVENT_LBUTTONDOWN:
        coord = userdata["coord"]
        dist_count = userdata["dist_count"]
        num_dist = userdata["num_dist"]
        if coord is None:
            coord = np.array((x, y))
            print(coord, file=stderr)
        else:
            last_coord = coord
            coord = np.array((x, y))
            dist = norm(last_coord - coord)
            print(coord, file=stderr)
            print(f"dist: {dist} px", file=stderr)
            userdata["output_dist"].append(dist)
            coord = None
            dist_count += 1
            if dist_count == num_dist:
                userdata["completed"] = True
        userdata["coord"] = coord
        userdata["dist_count"] = dist_count


def calibrate(auto_cal, node_color_code, file_timestamp, n_pairs=None):
    coord = None
    num_dist = n_pairs
    dist_count = 0
    exit_stat = 1
    output = None

    cv2.namedWindow(WINNAME)
    vid = cv2.VideoCapture(0)
    vid.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_Y_MAX)
    vid.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_X_MAX)
    if auto_cal:
        ret, frame = vid.read()
        cal_nodes = find_node(frame, node_color_code, CALIBRATION_NUM_NODES)
        if len(cal_nodes) != CALIBRATION_NUM_NODES:
            print(
                "Cannot detect indicated number of nodes:",
                CALIBRATION_NUM_NODES,
                file=stderr,
            )
            exit_stat = 1
            return exit_stat == 0, output
        for node in cal_nodes:
            cv2.circle(frame, node, 5, COLOR_MAP[node_color_code], 2, -1)
        print(
            "Press 'c' to confirm calibration, or 'q' to recalibrate",
            file=stderr,
        )
        while True:
            cv2.imshow(WINNAME, frame)
            key = cv2.waitKey(1) & 0xFF
            if key == ord("q"):
                break
            if key == ord("c"):
                dist = norm(np.array(cal_nodes[0]) - np.array(cal_nodes[1]))
                print(f"dist={dist} px", file=stderr)
                output = dist
                exit_stat = 0
                break
    else:
        userdata = {
            "coord": coord,
            "dist_count": dist_count,
            "num_dist": num_dist,
            "output_dist": [],
            "completed": False,
        }
        cv2.setMouseCallback(WINNAME, get_coord, userdata)
        while True:
            ret, frame = vid.read()
            cv2.imshow(WINNAME, frame)
            if userdata["completed"]:
                exit_stat = 0
                break
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
        output = userdata["output_dist"]

    vid.release()
    cv2.destroyAllWindows()

    if exit_stat == 0:
        np.save(os.path.join(file_timestamp, "calibrate"), cal_nodes)
    return exit_stat == 0, output
