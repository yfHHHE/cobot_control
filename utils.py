import cv2
from cobot_controller import MyCobotController 
from aruco import ArucoDetector
aruco_detector = ArucoDetector()

class VideoController:
    def __init__(self,detector) -> None:
        self.detector = detector
        self.mycobot = MyCobotController('/dev/ttyTHS1', 1000000,aruco_detector)


    def pause_video(self):
        """
        Pauses the video feed until the 'p' key is pressed again.
        """
        print("Video paused. Press 'p' to resume.")
        while True:
            if cv2.waitKey(1) & 0xFF == ord('p'):
                print("Video resumed.")
                break

    def exit_video(self):
        """
        Exits the video feed and closes all OpenCV windows.
        """
        print("Exiting video.")
        cv2.destroyAllWindows()

    def printcd(self):
        print(self.mycobot.get_coords())

    def onoff(self):
        self.mycobot.onoff()

    def findAngle(self):
        self.mycobot.findAngle(1,2)