import numpy as np
import matplotlib.pyplot as plt
import sys
import os
from utils import *


def view_pos_data(data):
    n_nodes = (data.shape[1] - 1) // 2
    print(f"n_nodes={n_nodes}\ndata=\n{data}")

    for i in range(n_nodes):
        plt.scatter(data[:,1+2*i], data[:,2+2*i], s=2, label=f"Node {i+1}")
    plt.title("Positions of Nodes")
    plt.xlabel("x [m]")
    plt.ylabel("y [m]")
    # plt.legend()
    # plt.savefig("./output/view_data/image")


def view_motor_data(data):
    plt.plot(data[:,0], data[:,-1])
    plt.title("Motor Speed")
    plt.xlabel("t [s]")
    plt.ylabel("Speed [rad/s]")
    # plt.savefig("./output/view_data/motor_image")


def view_data(data, label, save_dir):
    # label = os.path.basename(label)
    plt.figure(figsize=(8*PLOT_SCALE, 6*PLOT_SCALE))

    plt.subplot(211)
    view_pos_data(data)
    plt.subplot(212)
    view_motor_data(data)

    plt.suptitle("Collected Data")
    plt.tight_layout()
    plt.savefig(os.path.join(save_dir, f"{label}_img"))
    plt.clf()


if __name__ == "__main__":
    f_name = sys.argv[1]
    data = np.load(f_name)
    view_data(data, os.path.basename(f_name), "./output/view_data")
