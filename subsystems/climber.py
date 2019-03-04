"""
Ctrl-Z FRC Team 4096
FIRST Robotics Competition 2019
Code for robot "----"
contact@team4096.org
"""

import math
import time
import sys

import wpilib
import wpilib.command
import ctre
import networktables

import const

class Climber(wpilib.command.Subsystem):

	def __init__(self, robot):

		super().__init__('climber')
		self.robot = robot

		# set up motor controllers
		self.front_axle_motor = ctre.WPI_TalonSRX(const.CAN_MOTOR_CLIMBER_FRONT_AXLE)
		self.back_axle_motor = ctre.WPI_TalonSRX(const.CAN_MOTOR_CLIMBER_BACK_AXLE)
		self.front_axle_drive_motor = ctre.WPI_VictorSPX(const.CAN_MOTOR_CLIMBER_FRONT_AXLE_DRIVE)

		self.front_axle_motor.setInverted(False)
		self.back_axle_motor.setInverted(False)
		self.front_axle_drive_motor.setInverted(False)

		self.climber_kP = 0.0
		self.climber_kI = 0.0
		self.climber_kD = 0.0

		self.climber_pid = wpilib.PIDController(
		 	self.climber_kP,
		 	self.climber_kI,
		 	self.climber_kD,
		 	self.get_climber_pid_input,
			self.set_climber_pid_output,
		)

		# add methods for range, continuous, tolerance etc.
		self.climber_pid.reset()
		self.climber_pid.setOutputRange(-1, 1)
		self.climber_pid.setAbsoluteTolerance(100)
		self.climber_pid.setContinuous(False)

		self.stop_back_axle()
		self.stop_front_axle()
		self.stop_drive_front_axle()

		# set up solenoids
		self.front_axle_solenoid = wpilib.DoubleSolenoid(const.CAN_PCM_B, const.PCM_CLIMBER_FRONT_BRAKE_SOLENOID_1,
			const.PCM_CLIMBER_FRONT_BRAKE_SOLENOID_2)

		self.back_axle_solenoid = wpilib.DoubleSolenoid(const.CAN_PCM_A, const.PCM_CLIMBER_BACK_BRAKE_SOLENOID_1,
			const.PCM_CLIMBER_BACK_BRAKE_SOLENOID_2)

		"""
		self.set_front_brakes()
		self.set_back_brakes()
		"""

		# set up limit switches
		self.front_top_limit = wpilib.DigitalInput(const.DIO_CLIMBER_FRONT_TOP_LIMIT)
		self.front_bottom_limit = wpilib.DigitalInput(const.DIO_CLIMBER_FRONT_BOTTOM_LIMIT)
		self.back_top_limit = wpilib.DigitalInput(const.DIO_CLIMBER_BACK_TOP_LIMIT)
		self.back_bottom_limit = wpilib.DigitalInput(const.DIO_CLIMBER_BACK_BOTTOM_LIMIT)


	def run_front_axle(self, value):
		self.front_axle_motor.set(value)

	def stop_front_axle(self):
		self.run_front_axle(0)

	def run_back_axle(self, value):
		self.back_axle_motor.set(value)

	def stop_back_axle(self):
		self.run_back_axle(0)

	def drive_front_axle(self, value):
		self.front_axle_drive_motor.set(value)

	def stop_drive_front_axle(self):
		self.drive_front_axle(0)

	"""
	def set_front_brakes(self):
		self.front_axle_solenoid.set(1)

	def release_front_brakes(self):
		self.front_axle_solenoid.set(2)

	def set_back_brakes(self):
		self.back_axle_solenoid.set(1)

	def release_back_brakes(self):
		self.back_axle_solenoid.set(2)
	"""

	def front_top_hit(self):
		return not self.front_top_limit.get()

	def front_bottom_hit(self):
		return not self.front_bottom_limit.get()

	def back_top_hit(self):
		return not self.back_top_limit.get()

	def back_bottom_hit(self):
		return not self.back_bottom_limit.get()

	def get_climber_pid_input(self):
		return self.front_axle_motor.getSelectedSensorPosition() - self.back_axle_motor.getSelectedSensorPosition()

	def set_climber_pid_output(self, output):
		front_speed = 1
		back_speed = 1
		if output > 0:
			front_speed -= output
		if output < 0:
			back_speed += output
		self.run_front_axle(front_speed)
		self.run_back_axle(back_speed)

	def log( self ):
		self.robot.nt_robot.putString( 'Ultrasonic Front', '{0:.2f}'.format(self.robot.ultrasonic_front.getValue()))
		self.robot.nt_robot.putString( 'Ultrasonic Rear', '{0:.2f}'.format(self.robot.ultrasonic_rear.getValue()))

		self.robot.nt_robot.putString( 'Front Climber Encoder', '{0:.2f}'.format(self.front_axle_motor.getSelectedSensorPosition()))
		self.robot.nt_robot.putString( 'Back Climber Encoder', '{0:.2f}'.format(self.back_axle_motor.getSelectedSensorPosition()))