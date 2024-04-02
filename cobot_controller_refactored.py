
import time
from pymycobot.mycobot import MyCobot

class MyCobotController:
    def __init__(self, port='/dev/ttyTHS1', baudrate=1000000):
        self.mc = MyCobot(port, baudrate)

    def send_coords(self, coords, speed=30, mode=1):
        # Ensures that the coords is a list of exactly 6 elements
        if len(coords) != 6:
            raise ValueError("Coordinates must be a list of 6 elements.")
        self.mc.send_coords(coords, speed, mode)
        time.sleep(3)  # Wait for movement to complete

    def get_coords(self):
        return self.mc.get_coords()

# This simplification focuses on ensuring the interface to the cobot is clear and robust.
# It removes the aruco_detector dependency from this class, as the robotic control should be agnostic of the detection mechanism.
