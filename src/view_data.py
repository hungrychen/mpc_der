import numpy as np
import matplotlib.pyplot as plt
import sys


def view_data(data):
    n_nodes = (data.shape[1] - 1) // 2
    print(f"n_nodes={n_nodes}\ndata=\n{data}")
    for i in range(n_nodes):
        plt.scatter(data[:,1+2*i], data[:,2+2*i], s=2, label=f"Node {i+1}")
    plt.title("Collected Positions of Nodes")
    plt.xlabel("x [m]")
    plt.ylabel("y [m]")
    plt.legend()

    plt.savefig("./output/view_data/image")


if __name__ == "__main__":
    view_data(np.load(sys.argv[1]))
