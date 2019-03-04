"""
Ctrl-Z FRC Team 4096
FIRST Robotics Competition 2019
Code for robot "----"
contact@team4096.org
"""

import wpilib

###  IMPORTS ###

# Subsystems

# Commands
import commands.drivetrain
import commands.hatch
import commands.cargo
import commands.climber

# Controls
from customcontroller.xbox_command_controller import XboxCommandController

import const

## CONSTANTS ##

class OI:
	"""
	Operator Input - This class ties together controls and commands.
	"""
	def __init__(self, robot):
		self.robot = robot

		# Controllers
		# Xbox
		self.driver1 = XboxCommandController(0)
		self.driver2 = XboxCommandController(1)

		self.driver1.RIGHT_JOY_X.setDeadzone(.1)
		self.driver1.LEFT_JOY_Y.setDeadzone(.1)
		self.driver1.RIGHT_JOY_X.setInverted(True)

		self.driver1.addCustomButton('28-30 secs', lambda: 28 < self.robot.driverstation.getMatchTime() < 30
			and not self.robot.driverstaion.isAutonomous())

		self.driver2.LEFT_JOY_Y.setDeadzone(.1)
		self.driver2.LEFT_JOY_Y.setInverted(True)
		self.driver2.RIGHT_JOY_Y.setInverted(True)

		self.driver2.addCustomButton('Joystick_Up', lambda: self.driver2.RIGHT_JOY_Y() > .9)
		self.driver2.addCustomButton('Joystick_Down', lambda: self.driver2.RIGHT_JOY_Y() < -.9)
		self.driver2.addCustomButton('Joystick_Left', lambda: self.driver2.RIGHT_JOY_X() < -.9)
		self.driver2.addCustomButton('Joystick_Right', lambda: self.driver2.RIGHT_JOY_X() > .9)
		self.driver2.addCustomButton('Joystick_None', lambda: abs(self.driver2.RIGHT_JOY_X()) < .3 and abs(self.driver2.RIGHT_JOY_Y()) < .3)

		### COMMANDS ###

		# DRIVE COMMANDS #
		self.drive_command = commands.drivetrain.Drive_With_Tank_Values(
			self.robot,
			self.driver1.RIGHT_JOY_X,
			self.driver1.LEFT_JOY_Y,
		)

		# HATCH #
		self.hatch_command = commands.hatch.Strafe_Carriage(self.robot,
			self.driver2.BOTH_TRIGGERS
		)

		# CARGO #
		self.cargo_arm_command = commands.cargo.Run_Cargo_Arm(self.robot,
			self.driver2.LEFT_JOY_Y
		)

		# CLIMBER #

		# Set default commands
		self.robot.drive.setDefaultCommand(self.drive_command)
		self.robot.hatch.setDefaultCommand(self.hatch_command)
		self.robot.cargo.setDefaultCommand(self.cargo_arm_command)

		# Controller 1: driver
		self.driver1.POV.UP.whenActive(commands.climber.Auto_Stilts_Down(self.robot))
		self.driver1.POV.UP.whenInactive(commands.climber.Stop_Stilts_Up_and_Down(self.robot))

		self.driver1.Y.whenActive(commands.climber.Run_Both_Stilts_Down(self.robot, speed = 0.4))
		self.driver1.Y.whenInactive(commands.climber.Stop_Stilts_Up_and_Down(self.robot))

		self.driver1.A.whenActive(commands.climber.Run_Both_Stilts_Up(self.robot, speed = 0.4))
		self.driver1.A.whenInactive(commands.climber.Stop_Stilts_Up_and_Down(self.robot))

		self.driver1.X.whenActive(commands.climber.Run_Front_Stilts_Up(self.robot, speed = -0.4))
		self.driver1.X.whenInactive(commands.climber.Stop_Stilts_Up_and_Down(self.robot))

		self.driver1.B.whenActive(commands.climber.Run_Back_Stilts_Up(self.robot, speed = -0.4))
		self.driver1.B.whenInactive(commands.climber.Stop_Stilts_Up_and_Down(self.robot))

		self.driver1.RIGHT_BUMPER.whenActive(commands.climber.Drive_Front_Climber(self.robot, speed = 1))
		self.driver1.RIGHT_BUMPER.whenInactive(commands.climber.Stop_Stilts_Up_and_Down(self.robot))

		self.driver1.START.whenActive(lambda: self.robot.limelight.toggle_driver_mode())

		self.driver1.customButtons['28-30 secs'].whenActive(lambda: self.driver1.setRumble())
		self.driver1.customButtons['28-30 secs'].whenInactive(lambda: self.driver1.setRumble(0))

		# Controller 2: everything else
		# Cargo...
		self.driver2.RIGHT_BUMPER.whenActive(commands.cargo.Run_Cargo_Intake_Inward(self.robot, speed = 1))
		self.driver2.RIGHT_BUMPER.whenInactive(commands.cargo.Stop_Cargo_Intake(self.robot))

		self.driver2.LEFT_BUMPER.whenActive(commands.cargo.Run_Cargo_Intake_Outward(self.robot, speed = 1))
		self.driver2.LEFT_BUMPER.whenInactive(commands.cargo.Stop_Cargo_Intake(self.robot))

		self.driver2.START.whenActive(lambda: self.robot.cargo.toggle_manual_mode())

		self.driver2.customButtons['Joystick_Up'].whenActive(commands.cargo.Run_Cargo_Arm_Distance(self.robot, 35))
		self.driver2.customButtons['Joystick_Down'].whenActive(commands.cargo.Run_Cargo_Arm_Distance(self.robot, 5))
		self.driver2.customButtons['Joystick_Left'].whenActive(commands.cargo.Run_Cargo_Arm_Distance(self.robot, 90))
		self.driver2.customButtons['Joystick_Right'].whenActive(commands.cargo.Run_Cargo_Arm_Distance(self.robot, 135))
		self.driver2.customButtons['Joystick_None'].whenActive(commands.cargo.Stop_Cargo_Arm(self.robot))

		# Hatch...

		self.driver2.POV.UP.whenActive(commands.hatch.Push_Out_Carriage(self.robot))
		self.driver2.POV.DOWN.whenActive(commands.hatch.Pull_In_Carriage(self.robot))
		self.driver2.POV.LEFT.whenActive(commands.hatch.Close_Beak(self.robot))
		self.driver2.POV.RIGHT.whenActive(commands.hatch.Open_Beak(self.robot))

		self.driver2.A.whenActive(commands.hatch.Intake_Hatch(self.robot))
		self.driver2.Y.whenActive(commands.hatch.Place_Hatch(self.robot))

		self.driver2.B.whenActive(commands.hatch.Auto_Strafe_Carriage_To_Line(self.robot))
		self.driver2.X.whenActive(commands.hatch.Auto_Strafe_Carriage(self.robot, 5.5))
