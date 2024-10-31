import cv2
from utils import *
from motor_connection import Motor

A_1 = 0.3
A_2 = 0.5
W = 1.0
U_0 = 0.0
T_DELTA = 0.2

FILE = "output/pid_ptp/wide_pulse.txt"

f = open(FILE, "w")

config = read_config()
vid = cv2.VideoCapture(0)
motor = Motor(config["motor_ids"][0],
              config["port"],
              config["baudrate"],
              def_speed=config["motor_speeds"][0])



vid.release()
cv2.destroyAllWindows()
f.close()
