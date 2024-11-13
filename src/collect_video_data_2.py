from get_top_node import get_top_node
from collect_video_data import collect_video_data
from calibrate import calibrate
from utils import *


CONFIG_FILE = "./config/config_collect_data.json"


def main():
    print("\n***Running distance calibration***")
    config = read_config(CONFIG_FILE)
    node_offset_dist = config["node_offset_distance"]  # in m
    calibration_dist = config["calibration_distance"]  # in m

    calibrate_success = False
    while not calibrate_success:
        calibrate_success, cal_dist_px = calibrate(True, DEF_CALIBRATION_COLOR)
    m_per_px = calibration_dist / cal_dist_px
    print(f"cm_per_px={m_per_px}")

    print("\n***Running offset calibration")
    top_node_success = False
    while not top_node_success:
        top_node_success, top_node = get_top_node(config)
    origin_px = (top_node[0], top_node[1] - node_offset_dist / m_per_px)
    print(f"origin_px={origin_px}")

    print("\n***Running data collection***")
    collect_video_data(config, origin_px, m_per_px)


if __name__ == "__main__":
    main()
