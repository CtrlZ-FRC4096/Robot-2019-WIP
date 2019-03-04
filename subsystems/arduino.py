"""
Ctrl-Z FRC Team 4096
FIRST Robotics Competition 2019
Code for robot "------"
contact@team4096.org
"""
import math
import time
import sys

import wpilib
import wpilib.command
import networktables

import const
from enum import Enum

class Arduino(wpilib.command.Subsystem):

	class LedState(Enum):
		DEFUALT = 'a'
		HAVE_CARGO = 'b'
		END_GAME = 'c'

	def __init__(self, robot):
		super().__init__('arduino')
		self.table = networktables.NetworkTables.getTable("arduino")
		self.arduino_i2c = wpilib.I2C(wpilib.I2C.Port.kOnboard, const.ARDUINO_DEVICE_ADDRESS)
		self.robot = robot

		self.led_state = self.LedState.DEFUALT
		self.set_led_state(self.LedState.DEFUALT)


	def periodic(self):
		# if haveCargo():
		# 	self.set_led_state(self.LedState.HAVE_CARGO)
		#else
		if self.robot.driverstation.getMatchTime() < 30 and self.robot.driverstation.isOperatorControl():
			self.set_led_state(self.LedState.END_GAME)


	def get_line_sensor_value(self):
		if self.robot.isSimulation():
			return None

		try:
			line_data = self.robot.arduino_i2c.readOnly(1)
		except:
			return None

		if line_data[0] == 127:
			# Sensor doesn't see a line
			return None

		# It sees a line
		return line_data[0]


	def set_led_state(self, new_state: LedState):
		if self.robot.isSimulation():
			return None

		if self.led_state != new_state:
			self.led_state = new_state
			self.arduino_i2c.transaction([ord(new_state.value)], 1)

	def log(self):
		line_value = self.get_line_sensor_value()

		if line_value is None:
			line_value = -1

		self.robot.nt_robot.putNumber('Line Sensor', line_value)
		if line_value == -1:
			self.robot.nt_robot.putBoolean('Line Sensor Active', False)
		else:
			self.robot.nt_robot.putBoolean('Line Sensor Active', True)


