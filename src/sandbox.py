from collect_data import preview_data
import numpy as np


data = np.loadtxt("output/collect_data/data2.txt", skiprows=1, delimiter=",")
print(data)

preview_data(data)
