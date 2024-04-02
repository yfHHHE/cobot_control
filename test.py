from pymycobot.mycobot import MyCobot
import time

baudrate=1000000
mc = MyCobot('/dev/ttyTHS1', baudrate)
mc.power_on()
# mc.send_angle(1,30,20)
# time.sleep(3)
# a = [0,0,0,0,0,-50]
# mc.send_angles(a,20)
#mc.send_coords([180, -66.7, 300.2, -125.75, -40.18, -64.06],20,1)
b = mc.get_angles()
print(b)