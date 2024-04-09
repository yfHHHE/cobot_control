from pymycobot.mycobot import MyCobot
import time
from scipy.spatial.transform import Rotation as R
import numpy as np
import cv2
def adjust_robot_arm_orientation(marker_rvec, arm_euler_deg,ax):
    rotation_matrix, _ = cv2.Rodrigues(marker_rvec)

# Create a Rotation object from the rotation matrix
    rotation = R.from_matrix(rotation_matrix)
    euler_angles_deg = rotation.as_euler('xyz', degrees=True)
    pitch = euler_angles_deg[0]
    yaw = euler_angles_deg[1]
    roll = euler_angles_deg[2]

    if pitch > 0:
        result = pitch - 180
    else:
        result = pitch + 180
    if ax == 1:
        ans = apply_pitch_rotation(arm_euler_deg,-result)
    elif ax == 2:
        ans = apply_pitch_rotation(arm_euler_deg,roll,2)
    elif ax == 3:
        ans = apply_pitch_rotation(arm_euler_deg,-yaw,3)
    return ans

def apply_pitch_rotation(initial_euler_degrees, pitch_degrees,ax=1):
    """
    Apply a pitch rotation to the initial orientation defined by Euler angles.
    
    Parameters:
    - initial_euler_degrees: The initial orientation as Euler angles [x, y, z] in degrees.
    - pitch_degrees: The pitch rotation to apply around the X-axis in degrees.
    
    Returns:
    - The new orientation as Euler angles [x, y, z] in degrees after applying the pitch rotation.
    """
    # Convert initial Euler angles to quaternion
    q_initial = R.from_euler('xyz', initial_euler_degrees, degrees=True).as_quat()
    
    if ax==1:
    # Quaternion representing the pitch rotation around the X-axis
        q_pitch = R.from_euler('y', pitch_degrees, degrees=True).as_quat()
    if ax == 2:
        q_pitch = R.from_euler('x', pitch_degrees, degrees=True).as_quat()
    if ax == 3:
        q_pitch = R.from_euler('z', pitch_degrees, degrees=True).as_quat()
    
    # Combine the initial orientation with the pitch rotation by quaternion multiplication
    q_combined = R.from_quat(q_pitch) * R.from_quat(q_initial)
    
    # Convert the resulting quaternion back to Euler angles (in degrees)
    new_euler_angles_deg = q_combined.as_euler('xyz', degrees=True)
    
    return new_euler_angles_deg
def ao(marker_rvec, arm_euler_deg):
    """
    Adjust the robot arm's orientation based on a marker's rotation vector and initial arm Euler angles.
    
    Parameters:
    - marker_rvec: The rotation vector of the marker.
    - arm_euler_deg: The initial Euler angles (in degrees) of the robot arm as [roll, pitch, yaw].
    
    Returns:
    - The adjusted Euler angles of the robot arm as [roll, pitch, yaw] in degrees.
    """
    # Convert the marker's rotation vector to a rotation matrix
    
    # Create a Rotation object from the rotation matrix of the marker
    marker_rotation = R.from_euler('xyz', marker_rvec, degrees=True)
    
    # Convert the arm's initial Euler angles to a Rotation object
    arm_rotation = R.from_euler('xyz', arm_euler_deg, degrees=True)
    
    # Apply the marker's rotation to the arm's rotation
    # This assumes the marker's rotation should be applied directly to the arm's current orientation
    adjusted_rotation = marker_rotation * arm_rotation
    
    # Optionally, apply additional adjustments here if needed
    # For example, to adjust pitch (x), roll (y), and yaw (z) by specific degrees:
    # additional_rotation = R.from_euler('xyz', [pitch_deg, roll_deg, yaw_deg], degrees=True)
    # adjusted_rotation = additional_rotation * adjusted_rotation
    
    # Convert the final rotation back to Euler angles in degrees
    adjusted_euler_deg = adjusted_rotation.as_euler('xyz', degrees=True)
    
    return adjusted_euler_deg


#print("Adjusted Euler angles (roll, pitch, yaw):", adjusted_angles)
if __name__ == "__main__":
    baudrate=1000000
    mc = MyCobot('/dev/ttyTHS1', baudrate)

    # # # #mc.send_angles([0,0,0,40,0,-50],20)
    # # # # time.sleep(3)
    # # # # a = [0,0,0,0,0,-50]
    # # # # mc.send_angles(a,20)
    # # mc.send_coords([45.6, -60.5, 339.0, -3.87, 1.41, 171],20,1)
    # # # time.sleep(1)
    b = mc.get_coords()
    print(b)
    a = b[-3:]

    na = ao([9.63, 7,1.27],a)

    b[-3:] = na

    mc.send_coords(b,20,0)
