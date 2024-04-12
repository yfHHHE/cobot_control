
import cv2
from aruco import ArucoDetector
from pymycobot.mycobot import MyCobot
import time
import math

class VideoController:                            
    def __init__(self, video_source=0):
        self.detector = ArucoDetector()
        self.mycobot = MyCobot('/dev/ttyTHS1', 1000000)
        self.cap = cv2.VideoCapture(video_source)
        if not self.cap.isOpened():
            raise IOError("Could not open video source.")

    def process_frame(self):
        while True:
            ret, frame = self.cap.read()
            if not ret:
                print("Failed to grab frame.")
                break
            cv2.imshow('Frame', frame)
            cv2.waitKey(1)


    def align_markers_by_z(self,target_ids):
        while True:
            ret, frame = self.cap.read()
            if not ret:
                print("Failed to grab frame.")
                break
            
            markers = self.detector.detect_markers(frame)
            target_markers = [marker for marker in markers if marker.id in target_ids]
            if len(target_markers) == 2:
                # Assuming markers have a .z attribute for depth
                z_values = [marker.z for marker in target_markers]

                if not self.z_values_aligned(z_values):
                    adjustment = self.calculate_adjustment(z_values)
                    # Assuming you have a method to send this adjustment to the robot
                    self.mycobot.send_adjustment(adjustment)
                else:
                    print("Markers are aligned by z.")
                    break  # or continue for continuous adjustment
            else:
                print("Not enough markers detected. Adjusting robot to search...")
                self.mycobot.send_adjustment(10)
    def z_values_aligned(self, z_values, threshold=0.1):
        return abs(z_values[0] - z_values[1]) < threshold

    def calculate_adjustment(self, z_values):
        """Determine adjustment based on the z-values of the target markers."""
        # Placeholder for adjustment logic
        # Example: determine direction based on difference of z-values
        z_diff = z_values[0] - z_values[1]
        if z_diff > 0:
            return "move closer to marker with ID {target_ids[1]}"
        else:
            return "move closer to marker with ID {target_ids[0]}"
    
    def send_adjustment(self,adjustment):
        angle = None
        while not angle:
            angle = self.mc.get_angles()[3]
            time.sleep(0.5)
        if angle>-90:
            self.mc.send_angle(4,angle-adjustment,20)
            time.sleep(3)
        print(f"Adjusting robot angle by {adjustment} degrees.") 


    def release_resources(self):
        self.cap.release()
        cv2.destroyAllWindows()


    def move_forward(self, distance):  ### Version 3 to Remove Systematic Error
        coords= None
        while not coords:
            coords = self.mycobot.get_coords()
            time.sleep(0.5)
            
        current_coords = self.mycobot.get_coords()  # Get current coordinates
        print(current_coords)
        target_x = current_coords[0] + distance # Update target X coordinate

       ### We tried to remove the consistent error by just adding 2 and also reduced the time delay for a smoother transition
        new_coords= self.mycobot.send_coords([target_x, current_coords[1], current_coords[2]+2]+current_coords[-3:] , 30, 1)
        print(new_coords)
        time.sleep(0.1)  # Delay after movement


    def move_left(self,distance):
        coords= None
        while not coords:
            coords = self.mycobot.get_coords()
            time.sleep(0.5)
        
        coords[1] += distance
        self.mycobot.send_coords(coords,30,1)
        time.sleep(2)

    def printcoords(self):
        coords= None
        while not coords:
            coords = self.mycobot.get_coords()
            time.sleep(0.5)

        a=self.mycobot.get_coords()
        print(a)
    
    def increaseheight(self,distance):
        coords= None
        while not coords:
            coords = self.mycobot.get_coords()
            time.sleep(0.5)

        coords[2] += distance
        self.mycobot.send_coords(coords,30,1)
        time.sleep(2)

    def correctedheight(self,angle,distance):
        coords= None
        while not coords:
            coords = self.mycobot.get_coords()
            time.sleep(0.5)
        
        NewZ = distance / math.sin(angle)
        NewX= distance / math.tan(angle)
        coords[0]+=NewX
        coords[2]+=NewZ
        self.mycobot.send_coords(coords,30,1)
        time.sleep(2)
    
    def rotateclaw(self,angle):
        angles= None
        while not angles:
            angles = self.mycobot.mc.get_angles()
            time.sleep(0.5)

        angles[5] += angle
        self.mycobot.mc.send_angles(angles,30,1)
        time.sleep(2)
        

        

# This version of VideoController initializes with a video source and creates instances of ArucoDetector and MyCobotController.
# It introduces a process_frame method to encapsulate frame processing and marker detection logic