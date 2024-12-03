import pyax12
import pyax12.packet as pk
import pyax12.connection
import time


conn = pyax12.connection.Connection("/dev/ttyUSB0", 1000000,
                                    timeout=0.1,
                                    waiting_time=0.003)

conn.goto(1, 0, 1023)
time.sleep(2)
# print(conn.get_present_speed(1))

start_time = time.time()
start = time.monotonic()

# From ChatGPT
print("***")
conn.goto(1, 1023, 512)
while time.monotonic() - start < 3:
    # speed = conn.read_data(1, pk.PRESENT_SPEED, 2)
    # print(f"speed in binary: {speed}")
    print(f"t={time.monotonic() - start}", end=", ")
    print(f"sp={conn.get_present_speed(1)}")

print("***")
conn.goto(1, 0, 512)
while time.monotonic() - start < 6:
    # speed = conn.read_data(1, pk.PRESENT_SPEED, 2)
    # print(f"speed in binary: {speed}")
    print(f"t={time.monotonic() - start}", end=", ")
    print(f"sp={conn.get_present_speed(1)}")
