import pyax12.connection as ax12_conn


class Motor:
    def __init__(self, id, port, baudrate):
        self.id = id
        self.port = port
        self.baudrate = baudrate
        self.connection = ax12_conn.Connection(port, baudrate)

    def __del__(self):
        self.connection.close()
        
    def custom_move(self, target_pos, speed=1023):
        """
        Move to the target position. Position must be in the range
        (0, 1023). 0: most CW; 1023: most CCW
        """
        assert target_pos >= 0 and target_pos <= 1023
        self.connection.goto(self.id, target_pos, speed)


# For testing
if __name__ == "__main__":
    import time

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
