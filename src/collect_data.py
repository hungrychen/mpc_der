import time
import cv2
import numpy as np
import matplotlib.pyplot as plt
from find_node import find_node
from motor_connection import Motor
from utils import *


OUTPUT_FILE = "output/collect_data/data.txt"
INIT_POS = [0.6]
FINAL_POS = 0.4
WAITING_TOL = 0.005
MAX_TIME = 10.0 # Approximate, will exceed
# DT = 0.05
FPS = 30
NODES = 3


def preview_data(data_matrix):
    time = data_matrix[:,0]

    yellow_x = data_matrix[:,3]
    yellow_y = -data_matrix[:,4]
    red_x = data_matrix[:,5]
    red_y = -data_matrix[:,6]
    green_x = data_matrix[:,7]
    green_y = -data_matrix[:,8]

    plt.clf()
    plt.plot(yellow_x, yellow_y, c="y")
    plt.plot(red_x, red_y, c="r")
    plt.plot(green_x, green_y, c="g")
    plt.savefig("output/preview")
    plt.close()

    plt.clf()
    plt.eventplot(time, linewidths=0.1)
    plt.savefig("output/preview_time")
    plt.close()


def main():
    config = read_config("config_collect_data.json")
    motor_ids = config["motor_ids"]
    motor_speeds = config["motor_speeds"]
    port = config["port"]
    baudrate = config["baudrate"]
    num_nodes = config["num_nodes"]

    motors: list[Motor] = []
    for id, speed, pos in zip(motor_ids, motor_speeds, INIT_POS, strict=True):
        motor = Motor(id, port, baudrate, speed)
        motor.custom_move(pos)
        print("Remember to calibrate distance")
        print(f"INIT {id}")
        motors.append(motor)

    motors[0].wait_for_pos(WAITING_TOL)
    vid = cv2.VideoCapture(0)
    motors[0].custom_move(FINAL_POS)

    cols = int(MAX_TIME * (FPS + .1))
    data_matrix = np.zeros((cols, NODES*2 + 3))
    # dataMatrix[:,0] = np.linspace(0, MAX_TIME, num=cols, endpoint=False)
    it = 0
    start_time = time.monotonic()

    while it < cols:
        # curr_time = 0.0
        # while curr_time < dataMatrix[it,0]:
        ret, frame = vid.read()
        curr_time = time.monotonic()-start_time
            #  print(curr_time, dataMatrix[it,0], bool(curr_time < dataMatrix[it,0]))
        print(f"starting it {it},\t\tt = {curr_time:.4f}")

        # yellow, red, green: from center outwards
        if ret:
            yellow_node = find_node(frame, YELLOW, num_nodes["yellow"])
            red_node = find_node(frame, RED, num_nodes["red"])
            green_node = find_node(frame, GREEN, num_nodes["green"])

        if yellow_node and red_node and green_node:
            data_matrix[it,0] = curr_time

            data_matrix[it,3:5] = np.array(yellow_node)
            data_matrix[it,5:7] = np.array(red_node)
            data_matrix[it,7:] = np.array(green_node)

            data_matrix[it,1] = motors[0].get_connection().\
                get_present_speed(motor_ids[0]) # multiply by 0.111 to get rpm
            data_matrix[it,2] = motors[0].get_connection().\
                get_present_position(motor_ids[0]) # multiply by 0.29297 to get deg
        else:
            continue

        end_time = time.monotonic()-start_time
        if end_time != curr_time:
            print(f"ending it {it},\t\tend_time = {end_time:.4f}")
        it += 1

    motors[0].stop()
    with open(OUTPUT_FILE, "w") as f:
        print("time,present_speed,present_pos,node_x_1,node_y_1, "
              + "node_x_2,node_y_2, "
              + "node_x_3,node_y_4,node_x_4,node_y_4", file=f)
        
        for row in data_matrix:
            print(*(f"{num:.4f}" for num in row), sep=",", file=f)
        

    # motors[0].wait_for_pos(WAITING_TOL)
    # motors[1].wait_for_pos(WAITING_TOL)


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
    
    # motors[0].wait_for_pos(WAITING_TOL)
    vid.release()
    cv2.destroyAllWindows()

    preview_data(data_matrix)


if __name__ == "__main__":
    main()
    print("Done")
