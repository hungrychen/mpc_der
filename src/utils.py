import json


FRAME_X_MIN = 0
FRAME_X_MAX = 640
FRAME_Y_MIN = 0
FRAME_Y_MAX = 480

MOTOR_MIN_POS = 0
MOTOR_MAX_POS = 1023
MOTOR_MIN_SPEED = 0
MOTOR_MAX_SPEED = 1023

RED = 0
ORANGE = 1
YELLOW = 2
GREEN = 3
BLUE = 4
PURPLE = 5
BROWN = 6
BLACK = 7
PINK = 8


def read_config(filepath: str = "config.json"):
    with open(filepath) as f:
        config = json.load(f)
    return config


def clip(num, min, max):
    if num < min:
        return min
    if num > max:
        return max
    return num
