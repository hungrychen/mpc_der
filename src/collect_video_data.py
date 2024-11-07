import cv2
import time
import numpy as np
from find_node import find_node
from utils import *


def main():
    config = read_config("./config/config_collect_data.json")
    data_interval = config["data_interval"]
    num_nodes = config["num_nodes"]
    duration = config["duration"]
    show_video = config["show_video"]
    print(num_nodes)

    vid = cv2.VideoCapture(0)
    vid.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_Y_MAX)
    vid.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_X_MAX)

    data_r = int((DATA_BUFFER_EXTRA_SCALE * duration) / data_interval)
    data_c = 1 + num_nodes[DEF_EXPERIMENT_COLOR_STR] * 2
    data = np.empty((data_r, data_c))

    start_time = time.monotonic()
    prev_time = start_time
    it = 0
    while True:
        curr_time = time.monotonic()
        if (curr_time - prev_time >= data_interval):
            prev_time = curr_time
            timestamp = curr_time - start_time
            if timestamp > duration:
                break
            if it >= data_r:
                print("Warning: exceeded allocated data array space. Exiting")
                break
            ret, frame = vid.read()
            print(f"t = {timestamp:.4f} s", end=" | ")

            data[it, 0] = timestamp
            orange_nodes = find_node(
                frame,
                DEF_EXPERIMENT_COLOR,
                num_nodes[DEF_EXPERIMENT_COLOR_STR],
            )
            for i, node in enumerate(orange_nodes):
                data[it, 1+i*2] = node[0]
                data[it, 2+i*2] = node[1]
            print(orange_nodes)

            if show_video:
                for node in orange_nodes:
                    cv2.circle(frame, node, 5, BGR_ORANGE, 2, -1)
                cv2.imshow(WINNAME, frame)
                if cv2.waitKey(1) & 0xFF == ord("q"):
                    exit(1)

            it += 1

    file_timestamp = time.time()
    data = data[:it,:]
    np.save(f"./output/collect_video_data/data_{file_timestamp:.0f}", data)
    np.savetxt(
        f"./output/collect_video_data/data_{file_timestamp:.0f}.csv",
        data,
        delimiter=",",
    )


if __name__ == "__main__":
    main()
