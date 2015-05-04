#!/usr/bin/python

from Adafruit_BBIO	import GPIO
from Adafruit_BBIO	import PWM
from time			import sleep

# Refresh Rate
ScreenDisplay_delay = 1
IMU_delay = 0.05
IMUtoBT_delay = 0.03

# Initial PID
fp = open('/root/RollE/Stablizer.conf')
PID_data = [line.strip() for line in fp]
PID = [float(x) for x in PID_data]
is_PID_new = True
fp.close()

# Motor 1 Pins
Motor1_D1 = "P8_11"
Motor1_D2 = "P8_9"
Motor1_EN = "P9_14"

# Motor 2 Pins
Motor2_D1 = "P8_17"
Motor2_D2 = "P8_15"
Motor2_EN = "P8_19"

# Motor 3 Pins
Motor3_D1 = "P9_30"
Motor3_D2 = "P9_28"
Motor3_EN = "P9_21"

exitStatus = False

def cleanup(signum, frame):
	global exitStatus
	print "\nRollE, signing out."
	exitStatus = True

	sleep(0.2)
	GPIO.cleanup()
	PWM.cleanup()

	exit()
