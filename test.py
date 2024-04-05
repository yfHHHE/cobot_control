from pymycobot.mycobot import MyCobot
import time
#

# # #mc.send_angles([0,0,0,40,0,-50],20)
# # # time.sleep(3)
# # # a = [0,0,0,0,0,-50]
# # # mc.send_angles(a,20)
#mc.send_coords([179.2, -33.3, 294.6, -118.3, -48, -21],20,1)
# # time.sleep(1)
# b = mc.get_coords()
# print(b)
# # a = b[-3:]
from scipy.spatial.transform import Rotation as R
import numpy as np
def adjust_robot_arm_orientation(marker_rvec, arm_euler_deg):
    aruco_euler = np.array(marker_rvec)  # Detected ArUco code orientation
    robot_arm_euler = np.array(arm_euler_deg)  # Robot arm orientation

    # Convert to quaternions
    aruco_quat = R.from_rotvec(aruco_euler).as_quat()
    desired_quat = R.from_euler('xyz', [180, 0, 0], degrees=True).as_quat()

    # Calculate the rotation needed to align the ArUco code with the desired orientation
    rotation_needed = R.from_quat(desired_quat) * R.from_quat(aruco_quat)

    # Apply this rotation to the robot arm's current orientation
    robot_arm_quat = R.from_euler('xyz', robot_arm_euler, degrees=True).as_quat()
    new_robot_arm_quat = rotation_needed * R.from_quat(robot_arm_quat)

    # Convert the new robot arm orientation back to Euler angles
    new_robot_arm_euler = R.from_quat(new_robot_arm_quat.as_quat()).as_euler('xyz', degrees=True)

    return new_robot_arm_euler

def apply_pitch_rotation(initial_euler_degrees, pitch_degrees):
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
    
    # Quaternion representing the pitch rotation around the X-axis
    q_pitch = R.from_euler('y', pitch_degrees, degrees=True).as_quat()
    
    # Combine the initial orientation with the pitch rotation by quaternion multiplication
    q_combined = R.from_quat(q_pitch) * R.from_quat(q_initial)
    
    # Convert the resulting quaternion back to Euler angles (in degrees)
    new_euler_angles_deg = q_combined.as_euler('xyz', degrees=True)
    
    return new_euler_angles_deg


#na = apply_pitch_rotation(a, -20)

#b[-3:] = na

#mc.send_coords(b,20,0)

b = 2.8/3.14*180
print(b)