import subprocess
import sys
from get_top_node import get_top_node
from collect_video_data import collect_video_data
from utils import *


CONFIG_FILE = "./config/config_collect_data.json"


def main():
    print("\n***Running distance calibration***")
    config = read_config(CONFIG_FILE)
    node_offset_dist = config["node_offset_distance"]  # in m
    calibration_dist = config["calibration_distance"]  # in m

    calibrate_success = 1
    while calibrate_success != 0:
        proc = subprocess.run(
            ["./src/calibrate.py", "-a", str(DEF_CALIBRATION_COLOR)],
            stdout=subprocess.PIPE,
        )
        calibrate_success = proc.returncode
    cal_dist_px = float(proc.stdout)
    m_per_px = calibration_dist / cal_dist_px
    print(f"cm_per_px={m_per_px}")

    print("\n***Running offset calibration")
    top_node_success = False
    while not top_node_success:
        top_node_success, top_node = get_top_node(CONFIG_FILE)
    origin_px = (top_node[0], top_node[1] - node_offset_dist / m_per_px)

    print("\n***Running data collection***")
    video_data, video_raw_data = collect_video_data(origin_px, m_per_px)


if __name__ == "__main__":
    main()
