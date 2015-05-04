#!/usr/bin/python

import threading
import signal
import time
import config
from IMU			import IMU
from Bluetooth		import Bluetooth
from IMUtoBT		import IMUtoBT
from Motor			import Motor
from Stablizer		import Stablizer

print "RollE - A Ballbot"
print "Final Year Project"
print "Ghulam Ishaq Khan Institute of Engineering Sciences and Technology"
print "https://github.com/alyyousuf7/RollE"
print ""

signal.signal(signal.SIGTSTP, config.cleanup)
print "Press CTRL+Z to exit."
print ""

imu = IMU()
imu.start()

bt = Bluetooth()
bt.start()

imu2bt = IMUtoBT(imu, bt)
imu2bt.start()

motor1 = Motor(config.Motor1_D1, config.Motor1_D2, config.Motor1_EN, 0)
motor2 = Motor(config.Motor2_D1, config.Motor2_D2, config.Motor2_EN, 1)
motor3 = Motor(config.Motor3_D1, config.Motor3_D2, config.Motor3_EN, 2)

stablizer = Stablizer(imu, motor1, motor2, motor3)

# Send PID Values over Bluetooth
currentPID = "PID:%.2f,%.2f,%.2f\n" % tuple(config.PID) 
bt.write(currentPID)

while True:
	print imu.getData()
	time.sleep(config.ScreenDisplay_delay)