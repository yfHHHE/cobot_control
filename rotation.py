import cv2
import numpy as np

# Define a function to convert rotation vectors to degrees
def rvec_to_degrees(rvec):
    # Convert rotation vector to rotation matrix
    R, _ = cv2.Rodrigues(rvec)
    
    # Calculate Euler angles from rotation matrix
    sy = np.sqrt(R[0,0] * R[0,0] +  R[1,0] * R[1,0])
    singular = sy < 1e-6
    if not singular:
        x = np.arctan2(R[2,1], R[2,2])
        y = np.arctan2(-R[2,0], sy)
        z = np.arctan2(R[1,0], R[0,0])
    else:
        x = np.arctan2(-R[1,2], R[1,1])
        y = np.arctan2(-R[2,0], sy)
        z = 0

    # Convert Euler angles from radians to degrees
    x = np.degrees(x)
    y = np.degrees(y)
    z = np.degrees(z)
    
    return x, y, z

# Initialize the video capture
cap = cv2.VideoCapture(0)

# Load the predefined dictionary
dictionary = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_100)
parameters = cv2.aruco.DetectorParameters()
cameraMatrix= np.array([[992.40913116, 0, 605.19256803],
                      [0, 996.28675761, 343.67586117],
                      [0, 0, 1]])
distCoeffs= np.array([[0.02206642, 0.20438685, -0.00633739, -0.00140045, -0.85132748]])

while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    # Detect the markers in the image
    markerCorners, markerIds, rejectedCandidates = cv2.aruco.detectMarkers(frame, dictionary, parameters=parameters)
    frame = cv2.aruco.drawDetectedMarkers(frame, markerCorners, markerIds)
    
    if markerIds is not None:
        rvecs, tvecs, _ = cv2.aruco.estimatePoseSingleMarkers(markerCorners, 0.02, cameraMatrix, distCoeffs)
        for i, rvec in enumerate(rvecs):
            # Convert rotation vector to degrees
            x, y, z = rvec_to_degrees(rvec[0])
            
            # Display the XYZ angles next to the marker
            cv2.putText(frame, f"X: {x:.2f}, Y: {y:.2f}, Z: {z:.2f}", (int(markerCorners[i][0][0][0]), int(markerCorners[i][0][0][1] - 15)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    
    cv2.imshow('Frame', frame)
    
    # Break the loop when 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()