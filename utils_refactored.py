
import cv2
from aruco import ArucoDetector
from pymycobot.mycobot import MyCobot
from cobot_controller_refactored import MyCobotController
import time
from camera_feed import CameraFeed
    
class VideoController:
    def __init__(self, video_source=0):
        self.detector = ArucoDetector()
        self.mycobot = MyCobot('/dev/ttyTHS1', 1000000)
        self.camera_feed = CameraFeed(source=video_source)
        self.active = True

    def onoff(self):
        if self.mycobot.is_power_on():
            self.mycobot.power_off()
        else:
            self.mycobot.power_on()

    def stop_processing_frame(self):
        self.active = False

    def process_frame(self):
        detector = ArucoDetector()
        while self.active:
            ret, frame = self.camera_feed.get_frame()
            if not ret:
                print("Failed to grab frame.")
                break
            # Detect markers in the frame
            corners, ids, _ = detector.detect_marker_corners(frame)
        
        # If markers are detected, draw them
            if ids is not None:
                detector.draw_marker(frame, corners, ids)
            cv2.imshow('Live Video Feed', frame)

            # Break the loop if 'q' is pressed
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break


    def align_markers_by_z(self,target_ids):
        detector = ArucoDetector()
        self.mycobot.send_angles([0,0,0,0,0,-50.5],30)
        time.sleep(3)
        while True:
            if self.is_machine_stable():
                ret, frame = self.camera_feed.get_frame()
                if not ret or frame is None:
                    print("Failed to grab frame.")
                    break
                cv2.imshow('Live Video Feed', frame)
                cv2.waitKey(1)
                markers = detector.detect_markers(frame)
                target_markers = [marker for marker in markers if marker['id'] in target_ids]
                target_markers.sort(key=lambda marker: marker['id'])
                print(target_markers)

                if len(target_markers) == 2:
                    # Assuming markers have a .z attribute for depth
                    z_values = [marker['z'] for marker in target_markers]

                    if not self.z_values_aligned(z_values):
                        adjustment = self.calculate_adjustment(z_values)
                        # Assuming you have a method to send this adjustment to the robot
                        self.send_adjustment(adjustment)
                    else:
                        print("Markers are aligned by z.")
                        break  # or continue for continuous adjustment
                else:
                    print("Not enough markers detected. Adjusting robot to search...")
                    self.send_adjustment(10)
                cv2.imshow('Live Video Feed', frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
                # cv2.imshow('Live Video Feed', frame)
        self.active = True
        self.process_frame()
    def z_values_aligned(self, z_values, threshold=0.005):
        return abs(z_values[0] - z_values[1]) < threshold
    
    def is_machine_stable(self):
        # Here, you'd implement or call a method to check if the machine has stopped moving
        # For now, let's assume it returns True after a fixed delay, simulating a stability check
        time.sleep(2)  # Wait for the machine to potentially stabilize
        return True

    def calculate_adjustment(self, z_values):
        """Determine adjustment based on the z-values of the target markers."""
        # Placeholder for adjustment logic
        # Example: determine direction based on difference of z-values
        z_diff = z_values[0] - z_values[1]
        if z_diff < 0:
            return -1
        else:
            return 1
    
    def send_adjustment(self,adjustment):
        angle = None
        while not angle:
            angle = self.mycobot.get_angles()[3]
            time.sleep(0.5)
        if angle>-90:
            self.mycobot.send_angle(4,angle-adjustment,20)
            time.sleep(3)
        print(f"Adjusting robot angle by {adjustment} degrees.") 


    def release_resources(self):
        self.camera_feed.stop()
        cv2.destroyAllWindows()



    def move_forward(self,distance):
        coords= None
        while not coords:
            coords = self.mycobot.get_coords()
            time.sleep(0.5)
        
        coords[0] += distance
        self.mycobot.send_coords(coords,30,1)
        time.sleep(2)

    

# This version of VideoController initializes with a video source and creates instances of ArucoDetector and MyCobotController.
# It introduces a process_frame method to encapsulate frame processing and marker detection logic.
