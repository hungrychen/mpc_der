import numpy as np
import matplotlib.pyplot as plt
import sys


def view_data(data):
    n_nodes = (data.shape[1] - 1) // 2
    print(f"n_nodes={n_nodes}\ndata=\n{data}")

    plt.figure()
    for i in range(n_nodes):
        plt.scatter(data[:,1+2*i], data[:,2+2*i], s=2, label=f"Node {i+1}")
    plt.title("Collected Positions of Nodes")
    plt.xlabel("x [m]")
    plt.ylabel("y [m]")
    plt.legend()

    plt.savefig("./output/view_data/image")


def view_motor_data(data):
    plt.figure()
    plt.plot(data[:,0], data[:,-1])
    plt.savefig("./output/view_data/motor_image")


if __name__ == "__main__":
    data = np.load(sys.argv[1])
    view_data(data)
    view_motor_data(data)
