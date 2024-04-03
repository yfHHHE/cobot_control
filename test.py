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
print(b)