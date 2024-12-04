import json


MIN_NODE_SEPARATION = 20.0
# MAX_NODE_TO_NODE_PX = 80.
NO_NODE = -999.0

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

COLOR_MAP: dict[int, tuple[int, int, int]] = {
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
DEF_CALIBRATION_COLOR = BLUE
DEF_EXPERIMENT_COLOR = ORANGE
DEF_EXPERIMENT_COLOR_STR = "orange"

DATA_BUFFER_EXTRA_SCALE = 1.0
MIN_DATA_INTERVAL = 0.02

MOTOR_WAITING_TIME = 0.003

PLOT_SCALE = 1.2


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
