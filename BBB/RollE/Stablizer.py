#!/usr/bin/python

import threading
import math
import config
from time			import sleep
from datetime		import datetime
from PID			import PID

def singleton(class_):
	instances = {}
	def getinstance(*args, **kwargs):
		if class_ not in instances:
			instances[class_] = class_(*args, **kwargs)
		return instances[class_]
	return getinstance
	
@singleton
class Stablizer (threading.Thread):
	def __init__(self, imu, m1, m2, m3):
		threading.Thread.__init__(self)

		self.imu = imu
		self.m1 = m1
		self.m2 = m2
		self.m3 = m3

		self.pidX = PID()
		self.pidY = PID()
		self.pidZ = PID(P=0.0, I=0.0, D=0.0)

		self.pidX.setPoint(0.02) # in radians
		self.pidY.setPoint(0.03)
		self.pidZ.setPoint(0.0)

		self.start()
	
	def run(self):
		t = 0
		while not config.exitStatus:
			try:
				if config.is_PID_new == True:
					self.pidX.setKp(config.PID[0])
					self.pidX.setKi(config.PID[1])
					self.pidX.setKd(config.PID[2])
					self.pidX.setIntegrator(0)

					self.pidY.setKp(config.PID[0])
					self.pidY.setKi(config.PID[1])
					self.pidY.setKd(config.PID[2])
					self.pidY.setIntegrator(0)
			except AttributeError:
				pass

			data = self.imu.getData()

			roll = data['complementaryX'] + 5.5
			pitch = data['complementaryY'] - 3.4
			yaw = data['complementaryZ']

			x = self.pidX.update(math.sin(roll*math.pi/180.0))
			y = self.pidY.update(math.sin(pitch*math.pi/180.0))

			output = self.vector2Motor(x, y)

			self.m1.setSpeed(1.00*output[0])
			self.m2.setSpeed(1.00*output[1])
			self.m3.setSpeed(1.00*output[2])
			
			sleep(0.02)

		print "Stablizer Thread: Shutting down."

	def vector2Motor(self, x, y):
		phase_offset = 4.107860468 # Motor to IMU angle offset (786)
		magnitude = math.sqrt(x*x + y*y)
		angle = math.atan(x/y) if y != 0 else math.pi/2.0
		if y < 0:
			angle = angle + math.pi
		angle = angle + phase_offset

		return (magnitude*math.sin(angle + math.pi/3.0), magnitude*math.sin(angle + 5.0*math.pi/3.0), magnitude*math.sin(angle + math.pi))

if __name__ == "__main__":
	i = 0
	while i < 2*math.pi:
		x = math.sin(i)
		y = math.cos(i)
		print "%.3f, %.3f, %.3f" % (vector2Motor(x, y))
		i = i + math.pi/3.0