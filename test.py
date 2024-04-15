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
def ao2(euler_angles_deg, rvec):
    """
    Apply a rotation vector to the Euler angles of a robot arm to get a new orientation.

    Parameters:
    - euler_angles_deg: Current Euler angles of the robot arm as [roll, pitch, yaw] in degrees.
    - rvec: Rotation vector as [a, b, c], representing the axis-angle rotation (Rodrigues' rotation formula).

    Returns:
    - New Euler angles after applying the rotation vector, in degrees.
    """
    # Convert current Euler angles to a rotation object
    current_rotation = R.from_euler('xyz', euler_angles_deg, degrees=True)
    
    # Create a rotation object from the rotation vector
    additional_rotation = R.from_euler('xyz', rvec, degrees=True)
    
    # Combine the rotations
    new_rotation = additional_rotation * current_rotation
    
    # Convert the combined rotation back to Euler angles in degrees
    new_euler_angles_deg = new_rotation.as_euler('xyz', degrees=True)
    return new_euler_angles_deg


def euler_to_direction_vector(euler_angles_deg):
    """
    Convert Euler angles (in degrees) to a direction vector along which the end effector is pointing.
    
    Parameters:
    - euler_angles_deg: tuple or list of three numbers representing the Euler angles (roll, pitch, yaw).
    
    Returns:
    - A unit vector representing the direction in which the end effector is pointing.
    """
    # Convert Euler angles to a rotation matrix
    rotation = R.from_euler('xyz', euler_angles_deg, degrees=True)
    rotation_matrix = rotation.as_matrix()
    
    # In most robotic systems, the z-axis is the forward direction
    forward_direction = rotation_matrix @ np.array([0, 0, 1])  # Column for z-axis in rotation matrix
    return forward_direction

def move_robot_arm(current_position, direction_vector, distance):
    """
    Calculate the new position of the robot arm by moving it along the direction it is pointing.
    
    Parameters:
    - current_position: Current position of the robot arm's end effector as a 3-element list or array.
    - direction_vector: Unit vector representing the direction to move.
    - distance: Distance to move along the direction vector.
    
    Returns:
    - New position of the robot arm's end effector as a 3-element array.
    """
    # Compute the new position by adding the scaled direction vector to the current position
    new_position = current_position + distance * direction_vector
    return new_position
def rotate_around_forward_axis(euler_angles_deg, angle_deg):
    """
    Rotate the end effector around the axis it is currently pointing by a specified angle.
    
    Parameters:
    - euler_angles_deg: Current Euler angles of the robot arm's tip as [roll, pitch, yaw].
    - angle_deg: The angle in degrees to rotate around the forward axis.
    
    Returns:
    - A new set of Euler angles after the rotation.
    """
    # Get the forward direction vector from current Euler angles
    forward_direction = euler_to_direction_vector(euler_angles_deg)
    
    # Current rotation from Euler angles
    current_rotation = R.from_euler('xyz', euler_angles_deg, degrees=True)
    
    # Create a rotation about the forward axis by the specified angle
    additional_rotation = R.from_rotvec(forward_direction * np.deg2rad(angle_deg))
    
    # Combine the current rotation with the additional rotation
    new_rotation = additional_rotation * current_rotation
    
    # Convert back to Euler angles
    new_euler_angles_deg = new_rotation.as_euler('xyz', degrees=True)
    return new_euler_angles_deg
if __name__ == "__main__":
    baudrate=1000000
    mc = MyCobot('/dev/ttyTHS1', baudrate)
    mc.power_off()
    time.sleep(1)
    # print(mc.get_angles())
    # mc.send_angles([41.3, 37.61, -73.03, -4.57, -29.44, -25.75],20)
    # # # # time.sleep(3)
    # # # # a = [0,0,0,0,0,-50]
    # # # # mc.send_angles(a,20)
    # # mc.send_coords([45.6, -60.5, 339.0, -3.87, 1.41, 171],20,1)
    # # # time.sleep(1)
    b = mc.get_coords()
    print(b)
    # a = b[-3:]
    # c = b[:3]
    # po = euler_to_direction_vector(a)
    # nc = move_robot_arm(c,po,-10)
    # b[:3] = nc
    # # na = ao2(a,[-30,-3,2])

    # # b[-3:] = na

    # mc.send_coords(b,20,0)
