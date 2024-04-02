import time
from pymycobot.mycobot import MyCobot

class MyCobotController:
    def __init__(self, port='/dev/ttyTHS1', baudrate=1000000,aruco_detector = 1):
        self.mc = MyCobot(port, baudrate)
        self.aruco_detector = aruco_detector

    def send_coords(self, coords, speed=30, mode=1):
        self.mc.send_coords(coords, speed, mode)
        time.sleep(3)  # Wait for movement to complete

    def get_coords(self):
        while True:
            coords = self.mc.get_coords()
            time.sleep(1)
            try:
                if isinstance(coords[0], float):  # Check if coords received successfully
                    break
            except:
                continue
        return coords

    def set_gripper_value(self, value, speed=99, wait=False):
        self.mc.set_gripper_value(value, speed, wait)

    def adjust_height(self, height=0):
        if height:
            while True:
                coords = self.mc.get_coords()
                time.sleep(1)
                try:
                    if isinstance(coords[0], float):  # Check if coords received successfully
                        break
                except:
                    continue
            coords[2] += (coords[2]-height)
            self.mc.send_coords(coords, 50, 0)
    
    def adjust_x(self, x=0):
        if x:
            while True:
                coords = self.mc.get_coords()
                time.sleep(0.2)
                try:
                    if isinstance(coords[0], float):  # Check if coords received successfully
                        break
                except:
                    continue
            coords[0] += (coords[0]-x)
            self.mc.send_coords(coords, 50, 0)
    
    def adjust_y(self, y=0):
        if y:
            while True:
                coords = self.mc.get_coords()
                time.sleep(1)
                try:
                    if isinstance(coords[0], float):  # Check if coords received successfully
                        break
                except:
                    continue
            coords[1] += (coords[1]-y)
            self.mc.send_coords(coords, 50, 0)

    
    def onoff(self):
        if self.mc.is_power_on():
            self.mc.power_off()
        else:
            self.mc.power_on()

    def findAngle(self,marker_id_1, marker_id_2):
        self.mc.send_angles([0,0,0,0,0,-50.5],30)
        tolerance = 0.1
        angle_adjustment = 1  # Degree to adjust each time
        result1 = self.aruco_detector.get_average_tvec(marker_id_1)
        result2 = self.aruco_detector.get_average_tvec(marker_id_2)
        while result1 is None or result2 is None:
            self.adjust_robot_angle(angle_adjustment)
            result1 = self.aruco_detector.get_average_tvec(marker_id_1)
            result2 = self.aruco_detector.get_average_tvec(marker_id_2)
        
        _, _, z1 = self.aruco_detector.get_average_tvec(marker_id_1)
        _, _, z2 = self.aruco_detector.get_average_tvec(marker_id_2)
        
        while abs(z1 - z2) > tolerance:
            # Adjust the robot's angle
            self.adjust_robot_angle(angle_adjustment)
            
            # Re-measure Z values after the adjustment
            _, _, z1 = self.aruco_detector.get_average_tvec(marker_id_1)
            _, _, z2 = self.aruco_detector.get_average_tvec(marker_id_2)
            
            print(f"Adjusted angle. Z1: {z1}, Z2: {z2}")
        
        print("Final angle found. Z values are approximately equal.")

    def adjust_robot_angle(self, degrees):
        angle = None
        while not angle:
            angle = self.mc.get_angles()[3]
            time.sleep(0.5)
        if angle>-90:
            self.mc.send_angle(4,angle-1,20)
            time.sleep(1)
        print(f"Adjusting robot angle by {degrees} degrees.")   