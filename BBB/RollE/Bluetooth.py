#!/usr/bin/python

import threading
import Adafruit_BBIO.UART as UART
import config
import serial
from time			import sleep

class Bluetooth (threading.Thread):
	def __init__(self, port=1):
		threading.Thread.__init__(self)

		UART.setup(("UART%i" % port))

		self.serial = serial.Serial(port=("/dev/ttyO%i" % port), baudrate=115200, timeout=0.1)
		self.serial.close()
		self.serial.open()

		self.serial.write("Started\r\n")
	
	def run(self):
		while not config.exitStatus:
			message = self.read()
			if message != "":
				if message.startswith("PID:"):
					message = message[4:]
					try:
						config.PID = [float(x) for x in message.split(",")]
						config.is_PID_new = True
						fp = open('Stablizer.conf', 'w')
						fp.truncate()
						fp.write(message.replace(",", "\n"))
						fp.close()
					except:
						print "Failed to save Stablizer.conf"
						pass

				elif message.startswith("PID?"):
					currentPID = "PID:%.2f,%.2f,%.2f\n" % tuple(config.PID) 
					self.write(currentPID)

			sleep(config.IMU_delay)
		print "Bluetooth Thread: Shutting down."

	def write(self, message):
		if self.serial.isOpen():
			return self.serial.write(message)
		return False
	
	def read(self):
		if self.serial.isOpen():
			message = ""
			condition = True
			while condition and (not config.exitStatus):
				lastCh = self.serial.read()

				if len(lastCh) == 0:
					condition = False
				else:
					message += lastCh
					condition = True
			return message
		return False
