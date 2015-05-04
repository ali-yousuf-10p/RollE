#!/usr/bin/python

import config
from Adafruit_BBIO	import GPIO
from Adafruit_BBIO	import PWM
from MotorEncoder	import MotorEncoder

class Motor:
	def __init__(self, motor_pin_1, motor_pin_2, motor_pin_pwm, encoder_id):
		self.motor_pin_1 = motor_pin_1
		self.motor_pin_2 = motor_pin_2
		self.motor_pin_pwm = motor_pin_pwm

		self.encoder_id = encoder_id
		#self.encoder = MotorEncoder()

		GPIO.setup(self.motor_pin_1, GPIO.OUT)
		GPIO.setup(self.motor_pin_2, GPIO.OUT)
		PWM.start(self.motor_pin_pwm, 0, 1000)

	def setSpeed(self, speed):
		# Set Direction
		if speed >= 0:
			self.setDirectionForward()
		else:
			speed = -speed
			self.setDirectionBackward()

		# Set Speed (0-100)
		if speed > 100:
			speed = 100
		PWM.set_duty_cycle(self.motor_pin_pwm, speed)

	def setDirectionForward(self):
		GPIO.output(self.motor_pin_1, GPIO.HIGH)
		GPIO.output(self.motor_pin_2, GPIO.LOW)

	def setDirectionBackward(self):
		GPIO.output(self.motor_pin_1, GPIO.LOW)
		GPIO.output(self.motor_pin_2, GPIO.HIGH)

	def stop(self):
		PWM.set_duty_cycle(self.motor_pin_pwm, 0)
		GPIO.output(self.motor_pin_1, GPIO.HIGH)
		GPIO.output(self.motor_pin_2, GPIO.HIGH)

	def read(self):
		return self.encoder.read(self.encoder_id)

if __name__ == "__main__":
	from time import sleep
	motor = Motor("P8_11", "P8_9", "P9_14", 0)

	while True:
		print motor.read()
		sleep(1)