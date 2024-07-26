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
    def __init__(self,
                 id: int,
                 port: str,
                 baudrate: int,
                 def_speed: int = MOTOR_MAX_SPEED):
        """
        Provide the default speed as def_speed in the range (0, 1023)
        """
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
        self.connection.goto(
            self.id, self.connection.get_present_position(self.id))
        self.connection.close() # type: ignore

    def get_connection(self):
        """
        Direct connection object. Don't use if avoidable
        """
        return self.connection

    def get_pos(self):
        """Get the normalized position"""
        return self.connection.get_present_position(self.id) / MOTOR_MAX_POS
    
    def arrived_at_pos(self, tolerance):
        full_scale_tolerance = tolerance * MOTOR_MAX_POS
        curr_pos = self.connection.get_present_position(self.id)
        target_pos = self.connection.get_goal_position(self.id)
        # print(f"wait_for_pos: {curr_pos}, {target_pos}")
        return (curr_pos > target_pos-full_scale_tolerance
                and curr_pos < target_pos+full_scale_tolerance)
    
    def wait_for_pos(self, tolerance):
        """
        Warning: this blocks
        """
        full_scale_tolerance = tolerance * MOTOR_MAX_POS
        while True:
            curr_pos = self.connection.get_present_position(self.id)
            target_pos = self.connection.get_goal_position(self.id)
            # print(f"wait_for_pos: {curr_pos}, {target_pos}")
            if (curr_pos > target_pos-full_scale_tolerance
                    and curr_pos < target_pos+full_scale_tolerance):
                break

    def custom_move(self,
                    target_pos: float,
                    speed: int | None = None,
                    block=False,
                    block_tolerance=0.05):
        """
        Move to the target position.
        Provide the position in the range (0, 1)
        Provide the speed in the range (0, 1023)
        """
        self.connection.goto(self.id, int(target_pos * MOTOR_MAX_POS), # type: ignore
                             self.def_speed if speed is None else speed)
        print("Wrote move")
        if block:
            self.wait_for_pos(block_tolerance)

        # while block:
        #     pos = self.get_pos()
        #     print(pos, target_pos)
        #     if (pos > target_pos-block_tolerance
        #             and pos < target_pos+block_tolerance):
        #         break
        
    def adjust_move(self, adjustment: float, speed: int | None = None):
        """
        Add the adjustment value to the current position.
        Final position value will be clamped to the range (0, 1)
        """
        curr_pos = (self.connection.get_present_position(self.id)
                    / float(MOTOR_MAX_POS))
        target_pos = curr_pos + adjustment
        target_pos = clip(target_pos, 0., 1.)

        # print(f"adjust_move: moving to target_pos {target_pos}")
        self.custom_move(target_pos, speed)


# For testing
if __name__ == "__main__":
    ID = 1
    PORT = "/dev/ttyUSB0"
    BAUDRATE = 1000000

    motor = Motor(ID, PORT, BAUDRATE)
    
    motor.custom_move(500)
    time.sleep(1)

    # motor.custom_move(512)
    # time.sleep(1)

    motor.custom_move(512, 20)
    print("moving")
    time.sleep(3)
