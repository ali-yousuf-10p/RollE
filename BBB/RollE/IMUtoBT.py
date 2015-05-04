#!/usr/bin/python

import threading
import math
import config
from time			import sleep
from datetime		import datetime

IMUtoBTLock = threading.Lock()

class IMUtoBT (threading.Thread):
	def __init__(self, imu, bt):
		threading.Thread.__init__(self)

		self.imu = imu
		self.bt = bt
	
	def run(self):
		while not config.exitStatus:
			data = self.imu.getData()

			# Send Kalman X,Y with a checksum
			self.bt.write("a:%.2f,%.2f,%.2f,%.2f,%.2f,%.2f,%.2f,%.2f,%.2f\n" % (data['originalX'], data['originalY'], data['originalZ'], data['kalmanX'], data['kalmanY'], data['kalmanZ'], data['complementaryX'], data['complementaryY'], data['complementaryZ']))
			sleep(config.IMUtoBT_delay)

		print "IMUtoBT Thread: Shutting down."
