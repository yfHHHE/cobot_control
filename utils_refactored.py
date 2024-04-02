
import cv2
from aruco import ArucoDetector
from cobot_controller_refactored import MyCobotController

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

    def release_resources(self):
        self.cap.release()
        cv2.destroyAllWindows()

# This version of VideoController initializes with a video source and creates instances of ArucoDetector and MyCobotController.
# It introduces a process_frame method to encapsulate frame processing and marker detection logic.
