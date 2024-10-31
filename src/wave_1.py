import time
import math
from find_node import find_node
from motor_connection import Motor
from utils import *


OUTPUT_FILE = "output/snap_test/data.txt"
INIT_POS = [0.75]
WAITING_TOL = 0.005


def main():
    start_time = time.monotonic()
    config = read_config("wave.json")
    print(f"Read in the config: {config}")

    motor_ids = config["motor_ids"]
    print(f"Ensure that the motors with ids {motor_ids} are connected")

    motor_speeds = config["motor_speeds"]
    port = config["port"]
    baudrate = config["baudrate"]

    print("Initializing motors:")
    motors = {}
    for id, speed, pos in zip(motor_ids, motor_speeds, INIT_POS, strict=True):
        motor = Motor(id, port, baudrate, speed)
        motor.custom_move(pos, block=True)
        print(f"\tInitializing motor {id}")
        motors[id] = motor

    # Generate wave
    print("Generating sine wave")
    while True:
        curr_time = time.monotonic() - start_time
        wave_func_value = 0.5 * math.sin(7.1/2 * curr_time) + 0.5
        print(f"Time: {curr_time}")

        print(f"\tWave func: {wave_func_value}")

        motors[1].custom_move(wave_func_value)
        # motors[2].custom_move(1 - wave_func_value)

        print(f"\tPos of motor 1: {motors[1].get_pos()}")
        # print(f"\tPos of motor 2: {motors[2].get_pos()}")

        time.sleep(0.01)

    # Move to initial position
    # motors[0].wait_for_pos(WAITING_TOL)
    # motors[1].wait_for_pos(WAITING_TOL)
    # motors[0].custom_move(.25)
    # motors[1].custom_move(.75)
    # motors[0].custom_move(.25, speed=3)
    # motors[1].custom_move(.75, speed=3)
    # motors[0].wait_for_pos(WAITING_TOL)
    # motors[1].wait_for_pos(WAITING_TOL)

    # vid = cv2.VideoCapture(0)
    # with open(OUTPUT_FILE, "w") as f:
    #     print("time,motor1,motor2,node_x,node_y", file=f, flush=True)
    #     time_start = time.monotonic()

    #     while (not motors[0].arrived_at_pos(WAITING_TOL)
    #                or not motors[1].arrived_at_pos(WAITING_TOL)):
    #         ret, frame = vid.read()
    #         red_node_list = find_node(frame, RED, config["num_nodes"]["red"])

    #         if red_node_list:
    #             red_node = red_node_list[0]

    #             data_list = []
    #             data_list.append(time.monotonic() - time_start)
    #             data_list.append(motors[0].get_pos())
    #             data_list.append(motors[1].get_pos())
    #             data_list.append(red_node[0])
    #             data_list.append(red_node[1])

    #             print(*data_list, sep=",", file=f)
    
    # vid.release()
    # cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
    print("Done")
