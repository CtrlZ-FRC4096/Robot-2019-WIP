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

# Controls
from controls.joystick_pov import Joystick_POV
from controls.xbox_button import Xbox_Button
from controls.xbox_trigger import Xbox_Trigger
from commands.command_call import Command_Call

import const

## CONSTANTS ##

# Deadband
JOY_DEAD_BAND 			= 0.15

# Xbox Controller
# Buttons
XBOX_BTN_A				= 1
XBOX_BTN_B				= 2
XBOX_BTN_X				= 3
XBOX_BTN_Y				= 4
XBOX_BTN_LEFT_BUMPER	= 5
XBOX_BTN_RIGHT_BUMPER	= 6
XBOX_BTN_BACK 			= 7
XBOX_BTN_START 			= 8
XBOX_BTN_LEFT_STICK 	= 9
XBOX_BTN_RIGHT_STICK 	= 10
# Axes
XBOX_AXIS_LEFT_X        = 0
XBOX_AXIS_LEFT_Y		= 1
XBOX_AXIS_RIGHT_X		= 4
XBOX_AXIS_RIGHT_Y		= 5
XBOX_BTN_LEFT_TRIGGER	= 2
XBOX_BTN_RIGHT_TRIGGER	= 3

# D-Pad
JOY_POV_NONE			= -1
JOY_POV_UP				= 0
JOY_POV_UP_RIGHT		= 45
JOY_POV_RIGHT			= 90
JOY_POV_DOWN_RIGHT		= 135
JOY_POV_DOWN			= 180
JOY_POV_DOWN_LEFT		= 225
JOY_POV_LEFT			= 270
JOY_POV_UP_LEFT			= 315

INVERT_XBOX_LEFT_X		= True
INVERT_XBOX_LEFT_Y		= False
INVERT_XBOX_RIGHT_X		= True
INVERT_XBOX_RIGHT_Y		= True


class OI:
	"""
	Operator Input - This class ties together controls and commands.
	"""
	def __init__(self, robot):
		self.robot = robot

		# Controllers
		# Xbox
		self.xbox_controller_1 = controls.xbox_controller.Xbox_Controller(0)
		self.xbox_controller_2 = controls.xbox_controller.Xbox_Controller(1)

		### COMMANDS ###

		# DRIVE COMMANDS #
		self.drive_command = commands.drivetrain.Drive_With_Tank_Values(
			self.robot,
			self._get_axis(self.xbox_controller_1, controls.xbox_controller.XBOX_AXIS_RIGHT_X, inverted = INVERT_XBOX_RIGHT_X),
			self._get_axis(self.xbox_controller_1, controls.xbox_controller.XBOX_AXIS_LEFT_Y, inverted = INVERT_XBOX_LEFT_Y),
		)

		# HATCH #
		self.hatch_command = commands.hatch.Strafe_Carriage(self.robot,
			self._get_axis(self.xbox_controller_2, controls.xbox_controller.XBOX_AXIS_RIGHT_X)
		)

		# CARGO #
		self.cargo_arm_command = commands.cargo.Run_Cargo_Arm(self.robot,
			self._get_axis(self.xbox_controller_2, controls.xbox_controller.XBOX_AXIS_LEFT_Y, inverted = True)
		)

		# CLIMBER #

		# Set default commands
		self.robot.drive.setDefaultCommand(self.drive_command)
		self.robot.hatch.setDefaultCommand(self.hatch_command)
		self.robot.cargo.setDefaultCommand(self.cargo_arm_command)

		# Controller 1: driver
		self.both_climber_up = Xbox_Button(self.xbox_controller_1, XBOX_BTN_Y)
		self.both_climber_up.whenPressed(commands.climber.Run_Both_Climber_Up(self.robot, speed = 0.4))
		self.both_climber_up.whenReleased(commands.climber.Stop_Climber_Up_and_Down(self.robot))

		self.both_climber_down = Xbox_Button(self.xbox_controller_1, XBOX_BTN_A)
		self.both_climber_down.whenPressed(commands.climber.Run_Both_Climber_Down(self.robot, speed = 0.4))
		self.both_climber_down.whenReleased(commands.climber.Stop_Climber_Up_and_Down(self.robot))

		self.front_climber_down = Xbox_Button(self.xbox_controller_1, XBOX_BTN_X)
		self.front_climber_down.whenPressed(commands.climber.Run_Front_Climber_Down(self.robot, speed = -0.4))
		self.front_climber_down.whenReleased(commands.climber.Stop_Climber_Up_and_Down(self.robot))

		self.back_climber_down = Xbox_Button(self.xbox_controller_1, XBOX_BTN_B)
		self.back_climber_down.whenPressed(commands.climber.Run_Back_Climber_Down(self.robot, speed = -0.4))
		self.back_climber_down.whenReleased(commands.climber.Stop_Climber_Up_and_Down(self.robot))

		self.drive_front_climber_backwards = Xbox_Button(self.xbox_controller_1, XBOX_BTN_RIGHT_BUMPER)
		self.drive_front_climber_backwards.whenPressed(commands.climber.Drive_Front_Climber(self.robot, speed = 1))
		self.drive_front_climber_backwards.whenReleased(commands.climber.Stop_Climber_Up_and_Down(self.robot))


		# Controller 2: everything else

		# Cargo...
		self.cargo_inward = Xbox_Button(self.xbox_controller_2, XBOX_BTN_RIGHT_BUMPER)
		self.cargo_inward.whileHeld(commands.cargo.Run_Cargo_Intake_Inward(self.robot, speed = 1))
		self.cargo_inward.whenReleased(commands.cargo.Stop_Cargo_Intake(self.robot))

		self.cargo_outward = Xbox_Button(self.xbox_controller_2, XBOX_BTN_LEFT_BUMPER)
		self.cargo_outward.whileHeld(commands.cargo.Run_Cargo_Intake_Outward(self.robot, speed = 1))
		self.cargo_outward.whenReleased(commands.cargo.Stop_Cargo_Intake(self.robot))

		self.auto_cargo_arm = Joystick_POV(self.xbox_controller_2, JOY_POV_UP)
		self.auto_cargo_arm.whenPressed(commands.cargo.Run_Cargo_Arm_Distance(self.robot, 90))
		self.auto_cargo_arm.whenReleased(commands.cargo.Stop_Cargo_Arm(self.robot))

		# Hatch...
		self.push_out_carriage = Xbox_Button(self.xbox_controller_2, JOY_POV_UP)
		self.push_out_carriage.whenPressed(commands.hatch.Push_Out_Carriage(self.robot))

		self.pull_in_carriage = Xbox_Button(self.xbox_controller_2, JOY_POV_DOWN)
		self.pull_in_carriage.whenPressed(commands.hatch.Pull_In_Carriage(self.robot))

		self.close_beak = Xbox_Button(self.xbox_controller_2, XBOX_BTN_X)
		self.close_beak.whenPressed(commands.hatch.Close_Beak(self.robot))

		self.eat_hatch = Xbox_Button(self.xbox_controller_2, XBOX_BTN_A)
		self.eat_hatch.whenPressed(commands.hatch.Intake_Hatch(self.robot))

		self.place_hatch = Xbox_Button(self.xbox_controller_2, XBOX_BTN_Y)
		self.place_hatch.whenPressed(commands.hatch.Place_Hatch(self.robot))

		self.auto_strafe_hatch = Xbox_Button(self.xbox_controller_2, XBOX_BTN_B)
		self.auto_strafe_hatch.whenPressed(commands.hatch.Auto_Strafe_Carriage_To_Line(self.robot))

		# Commented below line out, because it will prematurely cancel the previous hatch command, the line above, and the auto strafe will stop before target is hit -AP
		# self.auto_strafe_hatch.whenReleased(commands.hatch.Strafe_Carriage(self.robot, self._get_axis(self.xbox_controller_2, controls.xbox_controller.XBOX_AXIS_RIGHT_X)))

	def _get_axis(self, joystick, axis, inverted = False):
		"""
		Handles inverted joy axes and dead band.
		"""
		def axis_func():
			val = joystick.getAxis(axis)

			if abs(val) < JOY_DEAD_BAND:
				return 0
			elif inverted:
				return -val

			return val

		return axis_func