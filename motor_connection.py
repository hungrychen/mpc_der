import pyax12.connection as ax12_conn
import serial.serialutil
import sys
import time
from utils import *

# If there is an error, check that the serial connection is good. 
# Ensure other programs are not using the same serial port.
# Check that the power switches are all on.
# If you get an error with a "little_endian_byte_seq", check that the
# motor is plugged in properly.


class Motor:
    def __init__(self, id, port, baudrate, def_speed=MOTOR_MAX_SPEED):
        self.id = id
        self.port = port
        self.baudrate = baudrate
        self.def_speed = def_speed
        self.connection = None
        while not self.connection:
            try:
                self.connection = ax12_conn.Connection(port, baudrate)
            except serial.serialutil.SerialException:
                print("Check serial connection", file=sys.stderr)
                time.sleep(1)

    def __del__(self):
        self.connection.close() # type: ignore
        
    def custom_move(self, target_pos, speed=None):
        """
        Move to the target position.
        Provide the position in the range (0, 1)
        """
        target_pos *= MOTOR_MAX_POS
        self.connection.goto(self.id, int(target_pos), # type: ignore
                             self.def_speed if speed is None else speed)
        
    def adjust_move(self, adjustment, speed=None):
        """
        Add the adjustment value to the current position.
        Final position value will be clamped to the range (0, 1)
        """
        curr_pos = (self.connection.get_present_position(self.id)
                    / float(MOTOR_MAX_POS))
        target_pos = curr_pos + adjustment
        if target_pos < 0.:
            target_pos = 0.
        if target_pos > 1.:
            target_pos = 1.
        
        # print(f"adjust_move: moving to target_pos {target_pos}")
        self.custom_move(target_pos, speed)


# For testing
if __name__ == "__main__":
    ID = 1
    PORT = "/dev/ttyUSB0"
    BAUDRATE = 1000000

    motor = Motor(ID, PORT, BAUDRATE)
    
    motor.custom_move(0)
    time.sleep(1)

    motor.custom_move(512)
    time.sleep(1)

    motor.custom_move(1023, 100)
    time.sleep(3)
