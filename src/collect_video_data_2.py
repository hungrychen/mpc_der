import time
import os
import sys
import zipfile
import numpy as np
from pyax12 import connection
from get_top_node import get_top_node
from collect_video_data import collect_video_data
from calibrate import calibrate
from utils import *


CONFIG_FILE = "./config/config_collect_data.json"


def main():
    config = read_config(CONFIG_FILE)

    file_timestamp = f"{time.time():.0f}"
    os.chdir("./output/collect_video_data")
    os.mkdir(file_timestamp)

    motor = connection.Connection(
        config["port"],
        config["baudrate"],
        waiting_time=MOTOR_WAITING_TIME,
    )
    motor_id = config["motor_ids"][0]
    if not motor.ping(motor_id):
        print("Motor connection problem", file=sys.stderr)
        return False
    motor.goto(motor_id, 512, 100)
    time.sleep(3)

    print(
        "\n***Running distance calibration***",
        "\nWait for the object to stop moving before proceeding",
    )
    node_offset_dist = config["node_offset_distance"]  # in m
    calibration_dist = config["calibration_distance"]  # in m

    calibrate_success = False
    while not calibrate_success:
        calibrate_success, cal_dist_px = calibrate(
            True, DEF_CALIBRATION_COLOR, file_timestamp
        )
    m_per_px = calibration_dist / cal_dist_px
    print(f"cm_per_px={m_per_px}")

    print("\n***Running offset calibration***")
    top_node_success = False
    while not top_node_success:
        top_node_success, top_node = get_top_node(config)
    origin_px = (top_node[0], top_node[1] - node_offset_dist / m_per_px)
    np.save(os.path.join(file_timestamp, "offset"), top_node)
    print(f"origin_px={origin_px}")

    print("\n***Running data collection***")
    data_success, _, _ = collect_video_data(
        config, origin_px, m_per_px, file_timestamp, use_motor=motor
    )

    if data_success:
        with zipfile.ZipFile(
            f"{file_timestamp}.zip", "x", zipfile.ZIP_DEFLATED
        ) as zf:
            for f in os.listdir(file_timestamp):
                zf.write(f"{file_timestamp}/{f}", f)

    return data_success


if __name__ == "__main__":
    main()
