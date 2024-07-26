import time
import cv2
from find_node import find_node
from motor_connection import Motor
from utils import *


OUTPUT_FILE = "output/snap_test/data.txt"
INIT_POS = [0.75, 0.25]
WAITING_TOL = 0.005


def main():
    config = read_config("config_snap.json")
    motor_ids = config["motor_ids"]
    motor_speeds = config["motor_speeds"]
    port = config["port"]
    baudrate = config["baudrate"]

    motors: list[Motor] = []
    for id, speed, pos in zip(motor_ids, motor_speeds, INIT_POS, strict=True):
        motor = Motor(id, port, baudrate, speed)
        motor.custom_move(pos)
        print(f"INIT {id}")
        motors.append(motor)

    motors[0].wait_for_pos(WAITING_TOL)
    motors[1].wait_for_pos(WAITING_TOL)

    motors[0].custom_move(.25, speed=2)
    motors[1].custom_move(.75, speed=2)
    
    # motors[0].wait_for_pos(WAITING_TOL)
    # motors[1].wait_for_pos(WAITING_TOL)

    vid = cv2.VideoCapture(0)

    with open(OUTPUT_FILE, "w") as f:
        print("time,motor1,motor2,node_x,node_y", file=f, flush=True)
        time_start = time.monotonic()

        while (not motors[0].arrived_at_pos(WAITING_TOL)
                   or not motors[1].arrived_at_pos(WAITING_TOL)):
            ret, frame = vid.read()
            red_node_list = find_node(frame, RED, config["num_nodes"]["red"])

            if red_node_list:
                red_node = red_node_list[0]

                data_list = []
                data_list.append(time.monotonic() - time_start)
                data_list.append(motors[0].get_pos())
                data_list.append(motors[1].get_pos())
                data_list.append(red_node[0])
                data_list.append(red_node[1])

                print(*data_list, sep=",", file=f)
    
    vid.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
    print("Done")
