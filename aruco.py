import numpy as np
import cv2
import math

class ArucoDetector:
    def __init__(self):
        self.aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_100)
        self.parameters = cv2.aruco.DetectorParameters()
        self.parameters.adaptiveThreshWinSizeMin = 3
        self.parameters.adaptiveThreshWinSizeMax = 23
        self.parameters.adaptiveThreshWinSizeStep = 10
        k = np.array([[992.40913116, 0, 605.19256803],
                      [0, 996.28675761, 343.67586117],
                      [0, 0, 1]])
        d = np.array([[0.02206642, 0.20438685, -0.00633739, -0.00140045, -0.85132748]])
        self.mtx = k
        self.dist = d
        self.marker_size = 0.02  # Adjusted to be consistent with estimation call
        self.tvecs_buffers = {}
        self.buffer_size = 10

    def add_to_buffer(self, id, tvec):
        if id not in self.tvecs_buffers:
            self.tvecs_buffers[id] = []
        self.tvecs_buffers[id].append(tvec)
        if len(self.tvecs_buffers[id]) > self.buffer_size:
            self.tvecs_buffers[id].pop(0)

    def get_average_tvec(self, id):
        if id in self.tvecs_buffers and len(self.tvecs_buffers[id]) > 0:
            return np.mean(self.tvecs_buffers[id], axis=0)
        return None

    def detect_marker_corners(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        corners, ids, rejectedImgPoints = cv2.aruco.detectMarkers(gray, self.aruco_dict, parameters=self.parameters)
        return corners, ids, rejectedImgPoints

    def draw_marker(self, frame, corners, ids):
        cv2.aruco.drawDetectedMarkers(frame, corners, ids)
        if ids is not None and corners is not None:
            rvecs, tvecs, _objPoints = cv2.aruco.estimatePoseSingleMarkers(corners, self.marker_size, self.mtx, self.dist)
            for i, id in enumerate(ids):
                self.add_to_buffer(id[0], tvecs[i][0])
                average_tvec = self.get_average_tvec(id[0])
                if average_tvec is not None:
                    cv2.drawFrameAxes(frame, self.mtx, self.dist, rvecs[i], tvecs[i], 0.01)
                    x, y, z = average_tvec * 100
                    
                    # Prepare texts for overlay, each coordinate on a separate line
                    overlay_texts = [
                        f"ID {id[0]}: X: {x:.2f}cm",
                        f"Y: {y:.2f}cm",
                        f"Z: {z:.2f}cm"
                    ]
                    
                    # Get the bottom left corner of the current marker
                    bottom_left_corner = tuple(corners[i][0][0].astype(int))
                    
                    # Starting position for the text, adjust as necessary to avoid overlay on the marker
                    text_position = (bottom_left_corner[0] + 20, bottom_left_corner[1] - 10)
                    
                    # Loop through each text line, adjusting the position for each
                    for line, overlay_text in enumerate(overlay_texts, start=1):
                        line_position = (text_position[0], text_position[1] - 20 * line) # Adjust spacing between lines
                        # Put the text on the frame, one line at a time
                        cv2.putText(frame, overlay_text, line_position, cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)


                    

    def calculate_angle_between_markers(self, id1, id2):
        """
        Calculates the angle between two Aruco markers identified by id1 and id2.
        
        Args:
            id1 (int): The ID of the first Aruco marker.
            id2 (int): The ID of the second Aruco marker.
        
        Returns:
            float: The angle between the two markers in degrees. Returns None if either marker is not found.
        """
        avg_tvec1 = self.get_average_tvec(id1)
        avg_tvec2 = self.get_average_tvec(id2)

        if avg_tvec1 is not None and avg_tvec2 is not None:
            # Calculate the differences in the x and y (or z) coordinates
            dx = avg_tvec2[0] - avg_tvec1[0]
            dy = avg_tvec2[1] - avg_tvec1[1]
            
            # Calculate the angle in radians
            angle_rad = math.atan2(dy, dx)
            
            # Convert the angle to degrees
            angle_deg = math.degrees(angle_rad)
            
            return angle_deg

        return None
