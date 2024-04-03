from pymycobot.mycobot import MyCobot
import time

baudrate=1000000
mc = MyCobot('/dev/ttyTHS1', baudrate)
mc.power_off()
#mc.send_angles([0,0,0,40,0,-50],20)
# time.sleep(3)
# a = [0,0,0,0,0,-50]
# mc.send_angles(a,20)
#mc.send_coords([87.2, -63.5, 361.4, -300, 45, 90],20,1)
time.sleep(1)
b = mc.get_coords()
a = b[-3:]
from scipy.spatial.transform import Rotation as R

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


na = apply_pitch_rotation(a, -20)

b[-3:] = na

#mc.send_coords(b,20,0)
