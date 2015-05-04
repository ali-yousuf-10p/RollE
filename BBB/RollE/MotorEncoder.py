#!/usr/bin/python

import psutil
import os
import threading
import config
import mmap
import ctypes
from Adafruit_BBIO	import GPIO
from time			import sleep

def singleton(class_):
	instances = {}
	def getinstance(*args, **kwargs):
		if class_ not in instances:
				instances[class_] = class_(*args, **kwargs)
		return instances[class_]
	return getinstance

@singleton
class MotorEncoder (threading.Thread):
	N = 3
	def __init__(self):
		threading.Thread.__init__(self)
		
		for x in xrange(self.N):
			self.position[x] = 0

		# Kill already running Encoder Service
		for p in psutil.process_iter():
			try:
				if p.name() == 'Encoder':
					p.kill()
			except psutil.Error:
				pass

		# Start Encoder Service
		#os.system("./Encoder &")

		# Open shared file
		#f = open("encoders.shm", "r+b")

		# Map the file to memory address (pointer)
		#buf = mmap.mmap(f.fileno(), 4*self.N, mmap.MAP_SHARED, mmap.PROT_WRITE | mmap.PROT_READ)

		#self.__ticks = [0] * self.N
		#self.position = [0] * self.N

		# Point N ints to an array element
		#for x in xrange(self.N):
		#	self.__ticks[x] = ctypes.c_int.from_buffer(buf, 4*x)

		# Start the thread
		#self.start()

	def run(self):
		while not config.exitStatus:
			#for x in xrange(self.N):
			#	self.position[x] = self.__ticks[x].value
			sleep(0.05)

	def read(self, n):
		if n < 3:
			return self.position[n]
		else:
			return -1

if __name__ == "__main__":
	enc2 = MotorEncoder()
	enc = MotorEncoder()

	while True:
		for x in xrange(3):
			print enc.read(x), "\t", 
		print ""
		sleep(0.5)