
import cv2
from aruco import ArucoDetector
from pymycobot.mycobot import MyCobot
from cobot_controller_refactored import MyCobotController
import time
from camera_feed import CameraFeed
import numpy as np
from test import adjust_robot_arm_orientation,ao
import threading
from scipy.spatial.transform import Rotation as R
import math
class VideoController:
    def __init__(self, video_source=0):
        self.detector = ArucoDetector()
        self.mycobot = MyCobot('/dev/ttyTHS1', 1000000)
        self.camera_feed = CameraFeed(source=video_source)
        self.thread = None
        self.active = False

    def move(self, distance,i): ### Utilising Loops to minimise changes in other coordinates
        coords= None
        while not coords:
            coords = self.mycobot.get_coords()
            time.sleep(0.5)
        coords[i] += distance
        self.mycobot.send_coords(coords, 30, 1)
    
    def onoff(self):
        if self.mycobot.is_power_on():
            self.mycobot.power_off()
        else:
            self.mycobot.power_on()
    def start_processing_frame(self,ax=1):
        if not self.active:
            self.active = True
            # self.thread = threading.Thread(target=self.process_frame)
            # self.thread.start()
            self.process_frame(ax)
    def stop_processing_frame(self):
        self.active = False
        # if self.thread is not None:
        #     self.thread.join()

    def process_frame(self,ax):
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
                detector.draw_marker(frame, corners, ids,ax)
            key = cv2.waitKey(1) & 0xFF
        
            if key == ord('o'):  # Start processing
        
                self.active=False
                break
            elif key == ord('r'):
                self.keep_point(6)
            elif key == ord('y'):
                print(self.get_rvecs(4))
            cv2.imshow('Live Video Feed', frame)

            # Break the loop if 'q' is pressed

    def align_cam(self,target_id):
        self.align_cam_1d(target_id,1)
        # self.move(40,2)
        # time.sleep(3)
        # self.move(-40,0)
        # time.sleep(3)
        # self.align_cam_1d(target_id,3)
        # time.sleep(3)
        # self.align_cam_1d(target_id,2)
        # time.sleep(2)
        # self.align_cam_1d(target_id,1)
    def get_rvecs(self, target_id):
        """
        Collects rvecs from the target ArUco marker over 10 frames and calculates their average.
        Breaks the loop if the target marker's rvec is None in ten consecutive frames.
        
        Parameters:
        - target_id: The ID of the target ArUco marker.
        
        Returns:
        - The average rvec of the target marker over 10 valid frames, or None if the marker 
          is not detected or consistently not detected in 10 consecutive frames.
        """
        rvecs_collected = []
        frames_processed = 0
        consecutive_failures = 0  # Counter for consecutive None rvecs
        time.sleep(1)
        while frames_processed < 10 and consecutive_failures < 100:
            ret, frame = self.camera_feed.get_frame()
            if not ret:
                print("Failed to grab frame.")
                continue
            rvec = self.detector.get_rvec_of_marker(frame, target_id)
            if rvec is not None:
                rvecs_collected.append(rvec[0])  # Assuming rvec[0] because rvec is returned as a 3x1 array
                frames_processed += 1
                consecutive_failures = 0  # Reset the failure counter on success
            else:
                consecutive_failures += 1  # Increment the failure counter

            if cv2.waitKey(1) & 0xFF == ord('q'):  # Allows for quitting the loop with 'q' key
                break

        if frames_processed < 10:
            print("Target marker not detected in 10 frames or detected inconsistently.")
            return None
        else:
            average_rvec = np.mean(rvecs_collected, axis=0)
            rotation_matrix, _ = cv2.Rodrigues(average_rvec)
            rotation = R.from_matrix(rotation_matrix)
            euler_angles_deg = rotation.as_euler('xyz', degrees=True)
        return euler_angles_deg

    def align_cam_1d(self, target_id,ax):
        """
        Collects rvecs from the target ArUco marker over 10 frames and calculates their average.
        Breaks the loop if the target marker's rvec is None in ten consecutive frames.
        
        Parameters:
        - target_id: The ID of the target ArUco marker.
        
        Returns:
        - The average rvec of the target marker over 10 valid frames, or None if the marker 
          is not detected or consistently not detected in 10 consecutive frames.
        """
        rvecs_collected = []
        frames_processed = 0
        consecutive_failures = 0  # Counter for consecutive None rvecs
        time.sleep(1)
        while frames_processed < 10 and consecutive_failures < 10:
            ret, frame = self.camera_feed.get_frame()
            if not ret:
                print("Failed to grab frame.")
                continue
            rvec = self.detector.get_rvec_of_marker(frame, target_id)
            if rvec is not None:
                rvecs_collected.append(rvec[0])  # Assuming rvec[0] because rvec is returned as a 3x1 array
                frames_processed += 1
                consecutive_failures = 0  # Reset the failure counter on success
            else:
                consecutive_failures += 1  # Increment the failure counter

            if cv2.waitKey(1) & 0xFF == ord('q'):  # Allows for quitting the loop with 'q' key
                break

        if frames_processed < 10:
            print("Target marker not detected in 10 frames or detected inconsistently.")
            return None
        else:
            average_rvec = np.mean(rvecs_collected, axis=0)
            rotation_matrix, _ = cv2.Rodrigues(average_rvec)
            rotation = R.from_matrix(rotation_matrix)
            euler_angles_deg = rotation.as_euler('xyz', degrees=True)
            print(np.degrees(average_rvec))
            print("Euler angles (degrees):", euler_angles_deg)
            if input("?") == 'y':
                co = None
                while co is None:
                    co=self.mycobot.get_coords()
                ang = co[-3:]
                nang = adjust_robot_arm_orientation(average_rvec,ang,ax)
                co[-3:]=nang
                print(co)
                self.mycobot.send_coords(co,20,1)
        # a = None
        # while not a:
        #     a = self.mycobot.get_coords()
        #     time.sleep(0.5)
        # cur_euler = a[-3:]
        # print(cur_euler)
        # new_euler = adjust_robot_arm_orientation(average_rvec,cur_euler)
        # print(new_euler)
    def keep_point(self,targets_ids):
        while True:
            marker_rvec = self.get_rvecs(targets_ids)
            if marker_rvec is None:
                print("no Aruco code detected")
                break
            y,z,x = marker_rvec
            if y > 0:
                y =  180 - y
            else:
                y = -180-y
            z=-z
            if abs(x) >20 or abs(y) > 45 or abs(z)>20:
                print("too tilted")
                continue
            print(x,y,z)
            arm_angle = None
            while not arm_angle:
                arm_angle = self.mycobot.get_coords()
            adjust_ang = ao([x,y,z],arm_angle[-3:])
            arm_angle[-3:] = adjust_ang
            self.mycobot.send_coords(arm_angle,20,1)
            time.sleep(3)
            

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
