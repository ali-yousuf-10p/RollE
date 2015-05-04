#!/usr/bin/python

from Adafruit_I2C	import Adafruit_I2C as I2C
from time		import sleep

def singleton(class_):
	instances = {}
	def getinstance(*args, **kwargs):
		if class_ not in instances:
			instances[class_] = class_(*args, **kwargs)
		return instances[class_]
	return getinstance

@singleton
class HMC5883L:
	deviceAddress = 0x1E	# HMC5883L I2C Address
	dataRegister = 0x03	# MPU6050 Data Address
	
	MAG0MAX = 603
	MAG0MIN = -578

	MAG1MAX = 542
	MAG1MIN = -701

	MAG2MAX = 547
	MAG2MIN = -556

	magOffset = [(MAG0MAX+MAG0MIN) / 2, (MAG1MAX+MAG1MIN) / 2, (MAG2MAX+MAG2MIN) / 2]

	def __init__(self):
		try:
			self.i2c = I2C(self.deviceAddress)
		except:
			print "HMC5883L not found."
		
		print "Connected to HMC5883L."
		
		self.magGain = [0 for x in xrange(3)]

		self.i2c.write8(0x02, 0x00)
		self.calibrate()
		sleep(0.1)
	
	def calibrate(self):
		self.i2c.write8(0x00, 0x11)
		sleep(0.1)
		magPosOff = self.read(False)

		self.i2c.write8(0x00, 0x12)
		sleep(0.1)
		magNegOff = self.read(False)

		self.i2c.write8(0x00, 0x10)
		
		self.magGain[0] = -2500 / float(magNegOff[0] - magPosOff[0])
		self.magGain[1] = -2500 / float(magNegOff[1] - magPosOff[1])
		self.magGain[2] = -2500 / float(magNegOff[2] - magPosOff[2])
	
	def read(self, calibrated = True):
		values = self.i2c.readList(self.dataRegister, 6)	
		
		magX = (values[0] << 8 | values[1]) - (65536 if values[0] >= 128 else 0)
		magZ = (values[2] << 8 | values[3]) - (65536 if values[2] >= 128 else 0)
		magY = (values[4] << 8 | values[5]) - (65536 if values[4] >= 128 else 0)
		
		if calibrated:
			magX = -magX*self.magGain[0] - self.magOffset[0]
			magY =  magY*self.magGain[1] - self.magOffset[1]
			magZ = -magZ*self.magGain[2] - self.magOffset[2]

		return [magX, magY, magZ]
