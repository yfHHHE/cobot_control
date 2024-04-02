
import cv2
from aruco import ArucoDetector
from cobot_controller_refactored import MyCobotController
import time
class VideoController:
    def __init__(self, video_source=0):
        self.detector = ArucoDetector()
        self.mycobot = MyCobotController('/dev/ttyTHS1', 1000000)
        self.cap = cv2.VideoCapture(video_source)
        if not self.cap.isOpened():
            raise IOError("Could not open video source.")

    def process_frame(self):
        while True:
            ret, frame = self.cap.read()
            if not ret:
                print("Failed to grab frame.")
                break
            # Detect markers in the frame
            markers = self.detector.detect_markers(frame)
            if markers:
                # Process detected markers...
                print("Markers detected:", markers)
                # Optionally, send commands to MyCobot based on detected markers


    def align_markers_by_z(self,target_ids):
        self.mc.send_angles([0,0,0,0,0,-50.5],30)
        time.wait(1)
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
            return -1
        else:
            return 1
    
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



    def move_forward(self,distance):
        coords= None
        while not coords:
            coords = self.mycobot.get_coords()
            time.sleep(0.5)
        
        coords[0] += 10
        self.mycobot.send_coords(coords,30,1)
        time.sleep(2)

    

# This version of VideoController initializes with a video source and creates instances of ArucoDetector and MyCobotController.
# It introduces a process_frame method to encapsulate frame processing and marker detection logic.
