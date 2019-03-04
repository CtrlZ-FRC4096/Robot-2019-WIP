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
import wpilib.timer
import wpilib.command
import ctre
import networktables

import const

class Cargo(wpilib.command.Subsystem):
	def __init__(self, robot):

		super().__init__('cargo')
		self.robot = robot

		self.manual_mode = False

		# set up motor controllers
		self.cargo_arm_motor = ctre.WPI_VictorSPX(const.CAN_MOTOR_CARGO_ARM)
		self.cargo_intake_motor = ctre.WPI_VictorSPX(const.CAN_MOTOR_CARGO_INTAKE)

		self.cargo_arm_motor.setInverted(True)
		self.cargo_intake_motor.setInverted(False)

		# set up solenoids
		self.cargo_brake = wpilib.DoubleSolenoid(
			const.CAN_PCM_A,
			const.PCM_CARGO_SOLENOID_BRAKE_1,
			const.PCM_CARGO_SOLENOID_BRAKE_2)

		# set up limit switches
		#self.limit_1 = wpilib.DigitalInput(const.DIO_CARGO_LIMIT_1)

		# set up potentiometer
		self.pot = wpilib.AnalogPotentiometer(
			const.AIN_CARGO_ARM_POT,
			const.CARGO_ARM_POT_MULTIPLIER,
			const.CARGO_ARM_POT_OFFSET
		)

		# set up arm PID
		self.arm_kP = 0
		self.arm_kI = 0.01
		self.arm_kD = 0.02

		self.arm_pid = wpilib.PIDController(
			self.arm_kP,
			self.arm_kI,
			self.arm_kD,
			self.get_arm_pid_input,
			self.set_arm_pid_output,
		)

		self.arm_pid_output = 0
		self.arm_pid.setInputRange(0, 135)
		self.arm_pid.setOutputRange(-1, 1)
		self.arm_pid.setAbsoluteTolerance(2.5)
		self.arm_pid.setContinuous(False)
		self.arm_pid.disable()

		# Timer for running average on intake motor current
		self._current_samples = []
		self._last_current_value = 0.0
		self.current_timer = wpilib.Timer()
		self.current_timer.start()
		self.current_timer_delay = 5.0		# times per second

	def toggle_manual_mode(self):
		if self.manual_mode == False:
			self.manual_mode = True

		elif self.manual_mode == True:
			self.manual_mode = False

	def run_arm(self, speed):
		if self.manual_mode == False:
			if speed == 0:
				speed = 0
			if speed < 0:
				if self.get_pot() < 0:
					speed = 0
			if speed > 0:
				if self.get_pot() > 130:
					speed = 0
			self.cargo_arm_motor.set(speed)

		elif self.manual_mode == True:
			self.cargo_arm_motor.set(speed)

	def stop_arm(self):
		self.run_arm(0)

	def run_intake(self, value):
		self.cargo_intake_motor.set(value)

	def stop_intake(self):
		self.run_intake(0)

	def current_threshold_hit(self):
		"""
		Calculate a running average of current values.
		"""

		new_current = self.robot.pdp.getCurrent(const.CARGO_PDP_ID)

		self._current_samples.append(new_current)

		if not self.current_timer.hasPeriodPassed(self.current_timer_delay):
			return self._last_current_value

		# Calculate new running average
		new_avg = sum(self._current_samples) / len(self._current_samples)

		self._current_samples = [ ]
		self._last_current_value = new_avg

		return new_avg > const.CARGO_INTAKE_THRESHOLD

	def set_brake(self):
		self.cargo_brake.set(1)

	def release_brake(self):
		self.cargo_brake.set(2)

	def get_pot(self):
		return self.pot.get()

	def get_arm_pid_input(self):
		return self.pot.get()

	def update_pid(self, p = None, i = None, d = None):
		# Updates the PID values
		if p:
			self.arm_kP = p
		if i:
			self.arm_kI = i
		if d:
			self.arm_kD = d

		self.arm_pid.setPID(self.arm_kP, self.arm_kI, self.arm_kD)

	def set_arm_pid_output(self, output):

		# Make sure we're outputing at least enough to move the cargo arm at all

		if output < 0:
			output = min(-const.CARGO_MIN, output)
		else:
			output = max(const.CARGO_MIN, output)

		if self.arm_pid.onTarget():
			output = 0

		self.arm_pid_output = output

		self.run_arm(self.arm_pid_output)

	def log(self):
		pass
		self.robot.nt_robot.putString("AnalogPot value", "{0:.2f}".format(self.pot.get()))
