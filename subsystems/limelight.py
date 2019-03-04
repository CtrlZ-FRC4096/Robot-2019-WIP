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

class Limelight(wpilib.command.Subsystem):
	def __init__(self, robot):
		super().__init__('limelight')

		self.robot = robot

		self.driver_camera_mode = const.DRIVER_CAMERA_MODE_DEFAULT
		self.table = networktables.NetworkTables.getTable("limelight")


	def get_angle_to_target(self):
		return self.table.getNumber( 'tx', None )


	def set_driver_mode(self, mode):
		self.driver_camera_mode = mode
		self.table.putNumber('camMode', mode)


	def toggle_driver_mode(self):
		if self.driver_camera_mode == const.DRIVER_CAMERA_MODE_ENABLED:
			self.set_driver_mode(const.DRIVER_CAMERA_MODE_DISABLED)
		else:
			self.set_driver_mode(const.DRIVER_CAMERA_MODE_ENABLED)


	def log(self):
		pass