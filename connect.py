from pymycobot.mycobot import MyCobot
import time
baudrate=1000000
mc = MyCobot('/dev/ttyTHS1', baudrate)

# Setup

# Send a si
# while True:
mc.set_basic_output(27,1)
    # print(1)
    # time.sleep(1)
    # mc.set_basic_output(5,1) # Signal off
    # time.sleep(1)
