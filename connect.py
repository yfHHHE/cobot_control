from pymycobot.mycobot import MyCobot
import time
baudrate=1000000
mc = MyCobot('/dev/ttyTHS1', baudrate)
mc.send_angles([40.95, 15.82, -39.72, -24.16, -20.83, -24.16],20)
print(mc.get_coords())
