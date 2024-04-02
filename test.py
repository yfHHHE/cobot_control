from pymycobot.mycobot import MyCobot
baudrate=1000000
mc = MyCobot('/dev/ttyTHS1', baudrate)
a = mc.is_power_on()
b = not a
print(b)