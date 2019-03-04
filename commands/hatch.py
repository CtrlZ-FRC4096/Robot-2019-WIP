"""
Ctrl-Z FRC Team 4096
FIRST Robotics Competition 2019
Code for robot "----"
contact@team4096.org
"""
from wpilib.command.commandgroup import CommandGroup
from wpilib.command.command import Command
from wpilib.command import WaitCommand
import wpilib

import subsystems.hatch

import const
import ctre

"""
HATCH STEPS:
1. Push
2. Open
3. Close
4. Pull
"""

"""
Step 1 command
"""
class Push_Out_Carriage(Command):
	def __init__(self, robot):
		super().__init__()
		self.robot = robot
		self.requires(self.robot.hatch)
		self.setInterruptible(True)

	def initialize(self):
		pass

	def execute(self):
		self.robot.hatch.push_out_carriage()

	def isFinished(self):
		return True

	def end(self):
		pass

	def isInterrupted(self):
		self.end()

class Pull_In_Carriage(Command):
	def __init__(self, robot):
		super().__init__()
		self.robot = robot
		self.requires(self.robot.hatch)
		self.setInterruptible(True)

	def initialize(self):
		pass

	def execute(self):
		self.robot.hatch.pull_in_carriage()

	def isFinished(self):
		return True

	def end(self):
		pass

	def isInterrupted(self):
		self.end()

class Open_Beak(Command):
	def __init__(self, robot):
		super().__init__()
		self.robot = robot
		self.requires(self.robot.hatch)
		self.setInterruptible(True)

	def initialize(self):
		pass

	def execute(self):
		self.robot.hatch.open_beak()

	def isFinished(self):
		return True

	def end(self):
		pass

	def isInterrupted(self):
		self.end()

class Close_Beak(Command):
	def __init__(self, robot):
		super().__init__()
		self.robot = robot
		self.requires(self.robot.hatch)
		self.setInterruptible(True)

	def initialize(self):
		pass

	def execute(self):
		self.robot.hatch.close_beak()

	def isFinished(self):
		return True

	def end(self):
		pass

	def isInterrupted(self):
		self.end()

class Place_Hatch(CommandGroup):
	'''
	Places Hatch
	'''
	def __init__(self, robot):
		super().__init__()

		self.robot = robot

		self.addSequential(Push_Out_Carriage(self.robot))
		self.addSequential(wpilib.command.WaitCommand(0.5))
		self.addSequential(Close_Beak(self.robot))
		self.addSequential(wpilib.command.WaitCommand(0.3))
		self.addSequential(Pull_In_Carriage(self.robot))

class Intake_Hatch(CommandGroup):
	'''
	Intake Hatch from Loading Station
	'''
	def __init__(self, robot):
		super().__init__()

		self.robot = robot
		self.addSequential(Push_Out_Carriage(self.robot))
		self.addSequential(wpilib.command.WaitCommand(0.5))
		self.addSequential(Open_Beak(self.robot))
		self.addSequential(wpilib.command.WaitCommand(0.4096))
		self.addSequential(Pull_In_Carriage(self.robot))

class Strafe_Carriage (Command):

	def __init__(self, robot, speed):

		super().__init__()

		self.robot = robot
		self.speed = speed

		self.requires(self.robot.hatch)
		self.setInterruptible(True)

	def initialize(self):
		pass

	def execute(self):
		self.robot.hatch.move_carriage(self.speed())

	def isFinished(self):
		return False

	def end(self):
		pass

	def interrupted(self):
		self.end()

class Auto_Strafe_Carriage(Command):
	def __init__(self, robot, setpoint):
		super().__init__()

		self.robot = robot
		self.setpoint = setpoint

		self.setInterruptible(True)
		self.requires(self.robot.hatch)
		self.setTimeout(2)

	def initialize(self):
		self.robot.hatch.carriage_pid.reset()
		self.robot.hatch.carriage_pid.setSetpoint(self.setpoint)
		self.robot.hatch.carriage_pid.enable()

	def execute(self):
		self.robot.hatch.move_carriage(self.robot.hatch.carriage_pid_output)

	def isFinished(self):
		on_target = self.robot.hatch.carriage_pid.onTarget()
		timed_out = self.isTimedOut()

		if timed_out:
			print('Hatch Carriage Timed out!')
		if on_target:
			self.distance_traveled = self.robot.hatch.get_carriage_pid_input()
			print('Hatch Carriage On Target! {0:.2f}'.format(self.distance_traveled))

		finished = on_target or timed_out
		return finished

	def end(self):
		self.robot.hatch.carriage_pid.reset()
		self.robot.hatch.stop_carriage()

	def interrupted(self):
		self.end()


class Auto_Strafe_Carriage_To_Line(Auto_Strafe_Carriage):
	def __init__(self, robot):
		super().__init__(robot, -11)

	def initialize(self):
		target_pos = self.robot.hatch.get_hatch_target_position()

		if target_pos is not None:
			self.setpoint = target_pos
			super().initialize()
