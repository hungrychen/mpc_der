import numpy as np
import matplotlib.pyplot as plt
import sys


def view_data(data):
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
    plt.ylabel("Speed")
    # plt.savefig("./output/view_data/motor_image")


def make_plot(data, f_name):
    sc = 1.3
    plt.figure(figsize=(8*sc, 6*sc))

    plt.subplot(211)
    view_data(data)
    plt.subplot(212)
    view_motor_data(data)

    plt.suptitle("Collected Data")
    plt.tight_layout()
    plt.savefig("./output/view_data/image")


if __name__ == "__main__":
    f_name = sys.argv[1]
    data = np.load(f_name)
    make_plot(data, f_name)
