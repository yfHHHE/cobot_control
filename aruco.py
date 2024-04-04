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
    def detect_markers(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        corners, ids, rejectedImgPoints = cv2.aruco.detectMarkers(gray, self.aruco_dict, parameters=self.parameters)
        markers = []
        if ids is not None:
            rvecs, tvecs, _ = cv2.aruco.estimatePoseSingleMarkers(corners, self.marker_size, self.mtx, self.dist)
            for i, corner, tvec in zip(ids, corners, tvecs):
                # tvec contains the translation vectors, where tvec[0][2] is the z-value (distance to the marker)
                markers.append({'id': i[0], 'corners': corner[0], 'z': tvec[0][2]})
        return markers

    def get_rvec_of_marker(self, frame, target_id):
        """
        Detects ArUco markers in the given frame and returns the rotation vector (rvec)
        of the marker with the specified ID.
        
        Parameters:
        - frame: The frame to detect the ArUco marker in.
        - target_id: The ID of the ArUco marker to find the rvec for.
        
        Returns:
        - The rotation vector (rvec) of the specified ArUco marker, if found. Otherwise, returns None.
        """
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        corners, ids, rejectedImgPoints = cv2.aruco.detectMarkers(gray, self.aruco_dict, parameters=self.parameters)
        
        if ids is not None:
            rvecs, tvecs, _objPoints = cv2.aruco.estimatePoseSingleMarkers(corners, self.marker_size, self.mtx, self.dist)
            for i, marker_id in enumerate(ids.flatten()):
                if marker_id == target_id:
                    return rvecs[i]  # Return the rotation vector of the specified marker
        return None

    def draw_marker(self, frame, corners, ids):
        cv2.aruco.drawDetectedMarkers(frame, corners, ids)
        if ids is not None and corners is not None:
            rvecs, tvecs, _objPoints = cv2.aruco.estimatePoseSingleMarkers(corners, self.marker_size, self.mtx, self.dist)
            for i, id in enumerate(ids):
                self.add_to_buffer(id[0], tvecs[i][0])
                average_tvec = self.get_average_tvec(id[0])
                if average_tvec is not None:
                    cv2.drawFrameAxes(frame, self.mtx, self.dist, rvecs[i], tvecs[i], 0.01)
                    R_j, _ = cv2.Rodrigues(rvecs[i])
                    # Convert rotation matrix to Euler angles
                    sy = math.sqrt(R_j[0,0] * R_j[0,0] +  R_j[1,0] * R_j[1,0])
                    singular = sy < 1e-6
                    if not singular:
                        x = math.atan2(R_j[2,1] , R_j[2,2])
                        y = math.atan2(-R_j[2,0], sy)
                        z = math.atan2(R_j[1,0], R_j[0,0])
                    else:
                        x = math.atan2(-R_j[1,2], R_j[1,1])
                        y = math.atan2(-R_j[2,0], sy)
                        z = 0
                    # Convert to degrees
                    x = np.degrees(x)
                    y = np.degrees(y)
                    z = np.degrees(z)
                    
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
