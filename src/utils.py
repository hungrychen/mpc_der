import json


FRAME_X_MIN = 0
FRAME_X_MAX = 960
FRAME_Y_MIN = 0
FRAME_Y_MAX = 720

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
BLACK = 7
PINK = 8

BGR_RED = (0, 0, 255)
BGR_ORANGE = (0, 165, 255)
BGR_YELLOW = (0, 255, 255)
BGR_GREEN = (0, 255, 0)
BGR_BLUE = (255, 0, 0)
BGR_PURPLE = (255, 0, 255)
BGR_BLACK = (0, 0, 0)
BGR_PINK = (50, 50, 255)

COLOR_MAP = {
    RED: BGR_RED,
    ORANGE: BGR_ORANGE,
    YELLOW: BGR_YELLOW,
    GREEN: BGR_GREEN,
    BLUE: BGR_BLUE,
    PURPLE: BGR_PURPLE,
    BLACK: BGR_BLACK,
    PINK: BGR_PINK,
}

WINNAME = "frame"
CALIBRATION_NUM_NODES = 2
CALIBRATION_COLOR = ORANGE


def read_config(filepath):
    with open(filepath) as f:
        config = json.load(f)
    return config


def clip(num, min, max):
    if num < min:
        return min
    if num > max:
        return max
    return num
