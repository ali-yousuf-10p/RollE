#!/usr/bin/python

import threading
import math
import config
from KalmanFilter	import KalmanFilter
from MPU6050		import MPU6050
from HMC5883L		import HMC5883L
from time			import sleep
from datetime		import datetime

IMULock = threading.Lock()

class IMU (threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)

		try:
			self.mpu6050 = MPU6050()
			self.hmc5883l = HMC5883L()

			# Original Values
			self.roll = 0
			self.pitch = 0
			self.yaw = 0

			# Kalman Filter
			self.kalmanX = KalmanFilter()
			self.kalmanY = KalmanFilter()
			self.kalmanZ = KalmanFilter()
			self.kalAngleX = 0
			self.kalAngleY = 0
			self.kalAngleZ = 0
			
			# Complementary Filter
			self.compAngleX = 0
			self.compAngleY = 0
			self.compAngleZ = 0
			
			# Only from Gyroscrope
			self.gyroAngleX = 0
			self.gyroAngleY = 0
			self.gyroAngleZ = 0
		except:
			print "Unable to create an instance for IMU."
			exit()
	
	def run(self):
		# Get the initial data
		[accX, accY, accZ, gyroX, gyroY, gyroZ, temperature] = self.mpu6050.read()
		[magX, magY, magZ] = self.hmc5883l.read()
		
		self.updatePitchRoll(accX, accY, accZ)
		self.updateYaw(magX, magY, magZ)
		
		# Set the initial angles (X: Roll; Y: Pitch, Z: Yaw)
		self.kalAngleX = self.kalmanX.setAngle(self.roll)
		self.kalAngleY = self.kalmanY.setAngle(self.pitch)
		self.kalAngleZ = self.kalmanZ.setAngle(self.yaw)
		self.compAngleX = self.roll
		self.compAngleY	= self.pitch
		self.compAngleZ = self.yaw
		self.gyroAngleX	= self.roll
		self.gyroAngleY	= self.pitch
		self.gyroAngleZ = self.yaw
		
		timer = datetime.now().microsecond
		
		while not config.exitStatus:
			IMULock.acquire()

			[accX, accY, accZ, gyroX, gyroY, gyroZ, temperature] = self.mpu6050.read()
			[magX, magY, magZ] = self.hmc5883l.read()

			dt = ( datetime.now().microsecond - timer ) / 1000000.0
			if dt < 0:
				dt = dt + 1
			timer = datetime.now().microsecond
			
			# PITCH AND ROLL
			self.updatePitchRoll(accX, accY, accZ)

			if (self.roll < -90 and self.kalAngleX > 90) or (self.roll > 90 and self.kalAngleY < -90):
				self.kalAngleX = self.kalmanX.setAngle(self.roll)
				self.compAngleX = self.roll
				self.gyroAngleX = self.roll
			else:
				self.kalAngleX = self.kalmanX.getAngle(self.roll, gyroX, dt)
			
			if math.fabs(self.kalAngleX) > 90:
				gyroY = -gyroY
			
			self.kalAngleY = self.kalmanY.getAngle(self.pitch, gyroY, dt)
			
			# YAW
			self.updateYaw(magX, magY, magZ)
			
			if (self.yaw < -90 and self.kalAngleZ > 90) or (self.yaw > 90 and self.kalAngleZ < -90):
				self.kalAngleZ = self.kalmanZ.setAngle(self.yaw)
				self.compAngleZ = self.yaw
				self.gyroAngleZ = self.yaw
			else:
				self.kalAngleZ = self.kalmanZ.getAngle(self.yaw, gyroZ, dt)

			self.gyroAngleX += gyroX * dt
			self.gyroAngleY += gyroY * dt
			self.gyroAngleZ += gyroZ * dt

			complementaryRate = 0.98
			self.compAngleX = complementaryRate * (self.compAngleX + gyroX * dt) + (1-complementaryRate) * self.roll
			self.compAngleY = complementaryRate * (self.compAngleY + gyroY * dt) + (1-complementaryRate) * self.pitch
			self.compAngleZ = complementaryRate * (self.compAngleZ + gyroZ * dt) + (1-complementaryRate) * self.yaw

			# Reset GyroAngle if its drifted too much
			if ((self.gyroAngleX < -180) or (self.gyroAngleX > 180)):
				self.gyroAngleX = self.kalAngleX
			if ((self.gyroAngleY < -180) or (self.gyroAngleY > 180)):
				self.gyroAngleY = self.kalAngleY
			if ((self.gyroAngleZ < -180) or (self.gyroAngleZ > 180)):
				self.gyroAngleZ = self.kalAngleZ
			
			IMULock.release()
			
			sleep(config.IMU_delay)

		print "IMU Thread: Shutting down."
	
	def updatePitchRoll(self, accX, accY, accZ):
		self.roll = math.degrees(math.atan2(accY, accZ))
		self.pitch = math.degrees(math.atan(-accX / math.sqrt(accY * accY + accZ * accZ)))
	
	def updateYaw(self, magX, magY, magZ):
		rollAngle = math.radians(self.kalAngleX)
		pitchAngle = math.radians(self.kalAngleY)
		
		Bfy = magZ * math.sin(rollAngle) - magY * math.cos(rollAngle)
		Bfx = magX * math.cos(pitchAngle) + magY * math.sin(pitchAngle) * math.sin(rollAngle) + magZ * math.sin(pitchAngle) * math.cos(rollAngle)
		
		self.yaw = math.degrees(math.atan2(-Bfy, Bfx))
	
	def getData(self):
		IMULock.acquire()
		data = {'originalX':self.roll, 'originalY':self.pitch, 'originalZ':self.yaw, 'kalmanX':self.kalAngleX, 'kalmanY':self.kalAngleY, 'kalmanZ':self.kalAngleZ, 'complementaryX':self.compAngleX, 'complementaryY':self.compAngleY, 'complementaryZ':self.compAngleZ}
		IMULock.release()
		return data
