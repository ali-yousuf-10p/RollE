#!/usr/bin/python

from Adafruit_I2C	import Adafruit_I2C as I2C

def singleton(class_):
	instances = {}
	def getinstance(*args, **kwargs):
		if class_ not in instances:
			instances[class_] = class_(*args, **kwargs)
		return instances[class_]
	return getinstance

@singleton
class MPU6050:
	deviceAddress = 0x68	# MPU6050 I2C Address
	dataRegister = 0x3B		# MPU6050 Data Address
	
	def __init__(self):
		try:
			self.i2c = I2C(self.deviceAddress)
		except:
			print "MPU6050 not found."
		
		print "Connected to MPU6050."
		
		self.i2c.writeList(0x19, [0x07, 0x00, 0x00, 0x00])
		self.i2c.write8(0x6B, 0x01)	# PLL with X axis gyroscope reference and disable sleep mode
		
		if self.i2c.readU8(0x75) != 0x68:
			print "Connected to UNKNOWN DEVICE."
			exit()
		
	def read(self):
		values = self.i2c.readList(self.dataRegister, 14)	
		
		accX = (values[0] << 8 | values[1]) - (65536 if values[0] >= 128 else 0)
		accY = (values[2] << 8 | values[3]) - (65536 if values[2] >= 128 else 0)
		accZ = (values[4] << 8 | values[5]) - (65536 if values[4] >= 128 else 0)
		tempRaw = (values[6] << 8 | values[7]) - (65536 if values[6] >= 128 else 0)
		gyroX = (values[8] << 8 | values[9]) - (65536 if values[8] >= 128 else 0)
		gyroY = (values[10] << 8 | values[11]) - (65536 if values[10] >= 128 else 0)
		gyroZ = (values[12] << 8 | values[13]) - (65536 if values[12] >= 128 else 0)
		
		gyroXrate = gyroX / 131.0
		gyroYrate = gyroY / 131.0
		gyroZrate = gyroZ / 131.0

		temperature = tempRaw / 340.0 + 36.53
		
		return [accX, accY, accZ, gyroXrate, gyroYrate, gyroZrate, temperature]
