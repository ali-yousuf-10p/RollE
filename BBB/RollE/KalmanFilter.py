#!/usr/bin/python

class KalmanFilter:
	"""Kalman Filter"""
	# We will set the variables like so, these can also be tuned by the user
	Q_angle = 0.001
	Q_bias = 0.003
	R_measure = 0.03

	def __init__(self):
		self.__angle = 0.0 # Reset the angle
		self.__bias = 0.0  # Reset bias
		
		# Since we assume that the bias is 0 and we know the starting angle (use setAngle), the error covariance matrix is set like so - see: http://en.wikipedia.org/wiki/Kalman_filter#Example_application.2C_technical
		self.__P = [[0 for x in xrange(2)] for x in xrange(2)]
		self.__K = [0 for x in xrange(2)]
		self.__P[0][0] = 0.0
		self.__P[0][1] = 0.0
		self.__P[1][0] = 0.0
		self.__P[1][1] = 0.0
		self.__K[0] = 0.0
		self.__K[0] = 0.0

	# The angle should be in degrees and the rate should be in degrees per second and the delta time in seconds
	def getAngle(self, newAngle, newRate, dt):
		# KasBot V2  -  Kalman filter module - http://www.x-firm.com/?page_id=145
		# Modified by Kristian Lauszus
		# See my blog post for more information: http://blog.tkjelectronics.dk/2012/09/a-practical-approach-to-kalman-filter-and-how-to-implement-it
		
		# Discrete Kalman filter time update equations - Time Update ("Predict")
		# Update xhat - Project the state ahead
		# Step 1
		self.__rate = newRate - self.__bias
		self.__angle += dt * self.__rate
		
		# Update estimation error covariance - Project the error covariance ahead
		# Step 2
		self.__P[0][0] += dt * (dt*self.__P[1][1] - self.__P[0][1] - self.__P[1][0] + KalmanFilter.Q_angle)
		self.__P[0][1] -= dt * self.__P[1][1]
		self.__P[1][0] -= dt * self.__P[1][1]
		self.__P[1][1] += KalmanFilter.Q_bias * dt

		# Discrete Kalman filter measurement update equations - Measurement Update ("Correct")
		# Calculate Kalman gain - Compute the Kalman gain
		# Step 4
		self.S = self.__P[0][0] + KalmanFilter.R_measure
		# Step 5
		self.__K[0] = self.__P[0][0] / self.S
		self.__K[1] = self.__P[1][0] / self.S

		# Calculate angle and bias - Update estimate with measurement zk (newAngle)
		# Step 3 */
		self.y = newAngle - self.__angle
		# Step 6 */
		self.__angle += self.__K[0] * self.y
		self.__bias += self.__K[1] * self.y

		# Calculate estimation error covariance - Update the error covariance
		# Step 7
		self.__P[0][0] -= self.__K[0] * self.__P[0][0]
		self.__P[0][1] -= self.__K[0] * self.__P[0][1]
		self.__P[1][0] -= self.__K[1] * self.__P[0][0]
		self.__P[1][1] -= self.__K[1] * self.__P[0][1]

		return self.__angle
	
	# Used to set angle, this should be set as the starting angle
	def setAngle(self, newAngle):
		self.__angle = newAngle
		return newAngle
	
	# Return the unbiased rate
	def getRate(self):
		return self.__rate
