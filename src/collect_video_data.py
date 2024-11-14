import cv2
import time
import sys
import numpy as np
from find_node import find_node
from utils import *


def collect_video_data(config, origin_px, m_per_px, save_files=True):
    success = True
    data_interval = config["data_interval"]
    if data_interval <= MIN_DATA_INTERVAL:
        data_interval = MIN_DATA_INTERVAL
    num_nodes = config["num_nodes"]
    duration = config["duration"]
    show_video = config["show_video"]
    rej_inc_node_set = config["reject_incomplete_node_set"]
    print(num_nodes)

    vid = cv2.VideoCapture(0)
    vid.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_Y_MAX)
    vid.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_X_MAX)

    data_r = int((DATA_BUFFER_EXTRA_SCALE * duration) / data_interval)
    data_c = 1 + num_nodes[DEF_EXPERIMENT_COLOR_STR] * 2
    data = np.full((data_r, data_c), NO_NODE)
    data_raw = np.full_like(data, NO_NODE)

    start_time = time.monotonic()
    prev_time = start_time
    it = 0
    while True:
        curr_time = time.monotonic()
        if curr_time - prev_time >= data_interval:
            if it >= data_r:
                print(
                    "Warning: exceeded allocated data array space. Exiting",
                    file=sys.stderr,
                )
                break

            exit_flag = False
            while True:
                ret, frame = vid.read()
                if not ret:
                    exit_flag = True
                    print("Check camera connection", file=sys.stderr)
                    break
                exp_nodes = find_node(
                    frame,
                    DEF_EXPERIMENT_COLOR,
                    num_nodes[DEF_EXPERIMENT_COLOR_STR],
                )
                valid_node_list = (
                    len(exp_nodes) == num_nodes[DEF_EXPERIMENT_COLOR_STR]
                )
                if not rej_inc_node_set or valid_node_list:
                    break
                print(
                    "Incomplete node set detected, recapturing frame",
                    file=sys.stderr,
                )
                curr_time = time.monotonic()
            if exit_flag:
                success = False
                break

            freq = 1 / (curr_time - prev_time)
            prev_time = curr_time
            timestamp = curr_time - start_time
            if timestamp > duration:
                break
            data[it, 0] = timestamp
            data_raw[it, 0] = timestamp
            # print(f"t = {timestamp:.4f} s", end=" | ")

            order_nodes(origin_px, exp_nodes)
            # print(f"orange_nodes={orange_nodes}", file=sys.stderr)
            for i, node in enumerate(exp_nodes):
                data_raw[it, 1 + i * 2] = node[0]
                data_raw[it, 2 + i * 2] = node[1]
                data[it, 1 + i * 2] = (node[0] - origin_px[0]) * m_per_px
                data[it, 2 + i * 2] = -(node[1] - origin_px[1]) * m_per_px
            print(f"n={len(exp_nodes)}: ", *[f"{d:.5f}" for d in data[it, :]])
            it += 1

            # Ref for showing text:
            # https://www.geeksforgeeks.org/python-opencv-cv2-puttext-method/
            if show_video:
                create_display(origin_px, frame, exp_nodes, freq)
                if cv2.waitKey(1) & 0xFF == ord("q"):
                    success = False
                    break

    data = data[:it, :]
    data_raw = data_raw[:it, :]
    if save_files:
        write_files(data, data_raw)

    return success, data, data_raw


def create_display(origin_px, frame, exp_nodes, freq):
    for node in exp_nodes:
        cv2.circle(frame, node, 5, COLOR_MAP[DEF_EXPERIMENT_COLOR], 2, -1)
    draw_node_connections(origin_px, exp_nodes, frame)
    cv2.putText(
        frame,
        f"Freq: {freq:.2f} Hz",
        (30, 30),
        cv2.FONT_HERSHEY_PLAIN,
        1.5,
        BGR_BLACK,
    )
    cv2.imshow(WINNAME, frame)


def write_files(data, data_raw):
    file_timestamp = time.time()
    np.save(
        f"./output/collect_video_data/{file_timestamp:.0f}_data",
        data,
    )
    np.savetxt(
        f"./output/collect_video_data/{file_timestamp:.0f}_data.csv",
        data,
        delimiter=",",
    )
    np.save(
        f"./output/collect_video_data/{file_timestamp:.0f}_dataraw",
        data_raw,
    )
    np.savetxt(
        f"./output/collect_video_data/{file_timestamp:.0f}_dataraw.csv",
        data_raw,
        delimiter=",",
    )


def order_nodes(origin_px, nodes_px):
    """
    Sort the nodes in increasing order of distance from the origin
    """
    origin_px_array = np.array(origin_px)
    key = lambda node: np.linalg.norm(np.array(node) - origin_px_array)
    nodes_px.sort(key=key)


def draw_node_connections(origin_px, nodes_px, frame):
    n_nodes = len(nodes_px)
    for i in range(n_nodes - 1):
        cv2.line(
            frame,
            nodes_px[i],
            nodes_px[i + 1],
            COLOR_MAP[DEF_EXPERIMENT_COLOR],
        )


if __name__ == "__main__":
    config = read_config("./config/config_collect_data.json")
    collect_video_data(config, (415, -10), 1, False)

    # nodes = [(404, 243), (400, 405), (398, 352), (407, 459), (401, 303), (406, 520)]
    # center = (404, np.float64(-122.02197735851058))
    # order_nodes(center, nodes)
    # print(nodes)
