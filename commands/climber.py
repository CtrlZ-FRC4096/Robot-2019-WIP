"""
Ctrl-Z FRC Team 4096
FIRST Robotics Competition 2019
Code for robot "----"
contact@team4096.org
"""

from commands.command_call import Command_Call

import ctre
from wpilib.command.command import Command
from wpilib.command.commandgroup import CommandGroup
from wpilib.command import WaitCommand
import wpilib

import const
import subsystems.climber

"""
TO DO:
- Step 1 with PID controller to keep position
of front and back to be exactly the same
- Ultrasonic sensors for Steps 2 & 4
"""

"""
CLIMB STEPS:
1. Run both axles downward so that the robot raises
2. Drive forward so that the first two wheels of the real drivetrain
	are on the platform
3. Run front axles upward so that they are all the way up
4. Drive forward until the center of mass is on the platform
	(use actual drivetrain)
5. Run back axle upward slightly
"""


class Run_Both_Stilts_Down(Command):
	"""
	Step 1 Command
	Use this method to run both climber axles downward,
	to raise the robot up at the beginning of the climb
	"""

	def __init__(self, robot, speed):

		super().__init__()

		self.robot = robot
		self.speed = speed

		self.requires(self.robot.climber)
		self.setInterruptible(True)

	def initialize(self):
		# self.robot.climber.release_front_brakes()
		# self.robot.climber.release_back_brakes()
		pass

	def execute(self):

		print(self.robot.climber.front_top_hit(), self.robot.climber.back_top_hit())

		if not self.robot.climber.front_top_hit():
			self.robot.climber.run_front_axle(self.speed)
		else:
			self.robot.climber.stop_front_axle()

		if not self.robot.climber.back_top_hit():
			self.robot.climber.run_back_axle(self.speed)
		else:
			self.robot.climber.stop_back_axle()

	def isFinished(self):
		return self.robot.climber.front_top_hit() and self.robot.climber.back_top_hit()
		# return False

	def end(self):
		self.robot.climber.stop_front_axle()
		self.robot.climber.stop_back_axle()

		# self.robot.climber.set_front_brakes()
		# self.robot.climber.set_back_brakes()

	def isInterrupted(self):
		self.end()

class Run_Both_Stilts_Up(Command):
	"""
	Step 1 Command
	Use this method to run both climber axles downward,
	to raise the robot up at the beginning of the climb
	"""

	def __init__(self, robot, speed):

		super().__init__()

		self.robot = robot
		self.speed = speed

		self.requires(self.robot.climber)
		self.setInterruptible(True)

	def initialize(self):
		# self.robot.climber.release_front_brakes()
		# self.robot.climber.release_back_brakes()
		pass

	def execute(self):
		print(self.robot.climber.front_bottom_hit(), self.robot.climber.back_bottom_hit())

		if not self.robot.climber.front_bottom_hit():
			self.robot.climber.run_front_axle(-self.speed)
		else:
			self.robot.climber.stop_front_axle()

		if not self.robot.climber.back_bottom_hit():
			self.robot.climber.run_back_axle(-self.speed)
		else:
			self.robot.climber.stop_back_axle()

	def isFinished(self):
		return self.robot.climber.front_bottom_hit() and self.robot.climber.back_bottom_hit()

	def end(self):
		self.robot.climber.stop_front_axle()
		self.robot.climber.stop_back_axle()

		# self.robot.climber.set_front_brakes()
		# self.robot.climber.set_back_brakes()

	def isInterrupted(self):
		self.end()

class Run_Front_Stilts_Up(Command):
	"""
	Step 3 Command --> brings front climber stilts up so that robot goes down
	"""
	def __init__(self, robot, speed):
		super().__init__()

		self.robot = robot
		self.speed = speed

		self.requires(self.robot.climber)
		self.setInterruptible(True)

	def initialize(self):
		#self.robot.climber.release_front_brakes()
		pass

	def execute(self):
		self.robot.climber.run_front_axle(self.speed)

	def isFinished(self):
		return self.robot.climber.front_bottom_hit()

	def end(self):
		self.robot.climber.stop_front_axle()
		#self.robot.climber.set_front_brakes()


class Run_Back_Stilts_Up(Command):
	"""
	Step 4 Command --> brings back climber stilts up so that robot goes down
	"""
	def __init__(self, robot, speed):
		super().__init__()

		self.robot = robot
		self.speed = speed

		self.requires(self.robot.climber)
		self.setInterruptible(True)

	def initialize(self):
		#self.robot.climber.release_back_brakes()
		pass

	def execute(self):
		self.robot.climber.run_back_axle(self.speed)

	def isFinished(self):
		return self.robot.climber.back_bottom_hit()

	def end(self):
		self.robot.climber.stop_back_axle()
		#self.robot.climber.set_back_brakes()

class Stop_Stilts_Up_and_Down(Command):
	def __init__(self, robot):
		super().__init__()

		self.robot = robot

		self.requires(self.robot.climber)
		self.setInterruptible(True)

	def initialize(self):
		self.robot.climber.stop_back_axle()
		self.robot.climber.stop_front_axle()
		#self.robot.climber.set_back_brakes()
		#self.robot.climber.set_front_brakes()

	def execute(self):
		pass

	def isFinished(self):
		return True


class Drive_Front_Climber(Command):
	"""
	Step 2 Command
	"""
	def __init__(self, robot, speed):
		super().__init__()

		self.robot = robot
		self.speed = speed

		self.requires(self.robot.climber)
		self.setInterruptible(True)

	def initialize(self):
		pass

	def execute(self):
		self.robot.climber.drive_front_axle(self.speed)

	def isFinished(self):
		pass

	def end(self):
		self.robot.climber.stop_drive_front_axle()


class Drive_Front_Climber_Until_Over_Hab(Command):
	"""
	Step 2 Command
	"""
	def __init__(self, robot, speed):
		super().__init__()

		self.robot = robot
		self.speed = speed

		self.ultrasonic_start_value = 0

		self.requires(self.robot.climber)
		self.setInterruptible(True)
		self.setTimeout(5)

	def initialize(self):
		self.ultrasonic_start_value = self.robot.ultrasonic_front.getValue()

	def execute(self):
		self.robot.climber.drive_front_axle(self.speed)

	def isFinished(self):
		# If ultrasonic value has dropped > N units, then it's over the next Hab platform
		over_next_level = self.ultrasonic_start_value - self.robot.ultrasonic_front.getValue() > const.ULTRASONIC_OVER_HAB_THRESHOLD

		return over_next_level or self.isTimedOut()

	def end(self):
		self.robot.climber.stop_drive_front_axle()


class Auto_Stilts_Down(Command):
	def __init__(self, robot):
		super().__init__()

		self.robot = robot

		self._front_position_start = 0
		self._back_position_start = 0

		self.requires(self.robot.climber)
		self.setInterruptible(True)

	def initialize(self):
		#self.robot.climber.release_back_brakes()
		#self.robot.climber.release_front_brakes()

		# Save starting position of each encoder
		self._front_position_start = self.robot.climber.front_axle_motor.getSelectedSensorPosition()
		self._back_position_start = self.robot.climber.back_axle_motor.getSelectedSensorPosition()

	def execute(self):
		front_speed = const.CLIMB_SPEED
		back_speed = const.CLIMB_SPEED

		# Get overall distance each has traveled since this command started
		front_travel_dist = self.robot.climber.front_axle_motor.getSelectedSensorPosition() - self._front_position_start
		back_travel_dist = self.robot.climber.back_axle_motor.getSelectedSensorPosition() - self._back_position_start

		# Get diff between both travel distances.
		# If one exceeds our tolerance, slow it down a bit to let the other catch up
		if front_travel_dist - back_travel_dist > const.CLIMB_DISTANCE_CORRECTION_TOLERANCE:
			front_speed *= const.CLIMB_SPEED_CORRECTION_MULTIPLIER
		elif back_travel_dist - front_travel_dist > const.CLIMB_DISTANCE_CORRECTION_TOLERANCE:
			back_speed *= const.CLIMB_SPEED_CORRECTION_MULTIPLIER

		# Set motor speeds
		self.robot.climber.run_front_axle(front_speed)
		self.robot.climber.run_back_axle(back_speed)

	def isFinished(self):
		return self.robot.climber.back_top_hit() or self.robot.climber.front_top_hit()

	def end(self):
		self.robot.climber.stop_back_axle()
		self.robot.climber.stop_front_axle()
		#self.robot.climber.set_back_brakes()
		#self.robot.climber.set_front_brakes()

	def interrupted(self):
		self.end()


class Auto_Stilts_Down_PID(Command):
	def __init__(self, robot):
		super().__init__()

		self.robot = robot

		self.requires(self.robot.climber)
		self.setInterruptible(True)

	def initialize(self):
		#self.robot.climber.release_back_brakes()
		#self.robot.climber.release_front_brakes()
		self.robot.climber.climber_pid.reset()
		self.robot.climber.climber_pid.enable()

	def execute(self):
		pass

	def isFinished(self):
		return self.robot.climber.back_top_hit() or self.robot.climber.front_top_hit()

	def end(self):
		self.robot.climber.climber_pid.reset()
		self.robot.climber.stop_back_axle()
		self.robot.climber.stop_front_axle()
		#self.robot.climber.set_back_brakes()
		#self.robot.climber.set_front_brakes()

	def interrupted(self):
		self.end()


