from pymycobot.mycobot import MyCobot
import time

baudrate=1000000
mc = MyCobot('/dev/ttyTHS1', baudrate)
# mc.power_off()
# #mc.send_angles([0,0,0,40,0,-50],20)
# # time.sleep(3)
# # a = [0,0,0,0,0,-50]
# # mc.send_angles(a,20)
mc.send_coords([45.6, -60.5, 339.0, -3.87, 1.41, 171],20,1)
# time.sleep(1)
b = mc.get_coords()
print(b)
# a = b[-3:]
from scipy.spatial.transform import Rotation as R

def adjust_robot_arm_orientation(marker_rvec, arm_euler_deg):
    # Convert marker's rotation vector to a quaternion
    marker_quat = R.from_rotvec(marker_rvec).as_quat()
    
    # Convert the robot arm's current orientation from Euler angles to a quaternion
    arm_quat = R.from_euler('zyx', arm_euler_deg, degrees=True).as_quat()
    
    # Calculate the adjustment needed by combining the marker's orientation with the
    # inverse of the arm's current orientation
    adjustment_quat = R.from_quat(marker_quat) * R.from_quat(arm_quat).inv()
    
    # Calculate the new arm orientation by applying the adjustment to the arm's current orientation
    new_arm_quat = adjustment_quat * R.from_quat(arm_quat)
    
    # Convert the new arm orientation back to Euler angles for the robot arm control
    new_arm_euler_deg = new_arm_quat.as_euler('zyx', degrees=True)
    
    return new_arm_euler_deg

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
