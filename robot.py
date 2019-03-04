#! python3

"""
Ctrl-Z FRC Team 4096
FIRST Robotics Competition 2019
Code for robot "----"
contact@team4096.org
"""

# Import our files
import cProfile
import logging
import os
import time

import wpilib
import wpilib.command
import wpilib.timer

import networktables

import const
import oi

import subsystems.drivetrain
import subsystems.limelight
import subsystems.hatch
import subsystems.cargo
import subsystems.climber
import subsystems.arduino


log = logging.getLogger('robot')


class Robot(wpilib.TimedRobot):
	"""
	Main robot class.

	This is the central object, holding instances of all the robot subsystem
	and sensor classes.

	It also contains the init & periodic methods for autonomous and
	teloperated modes, called during mode changes and repeatedly when those
	modes are active.

	The one instance of this class is also passed as an argument to the
	various other classes, so they have full access to all its properties.
	"""
	def robotInit(self):

		### Subsystems ###

		# Drivetrain
		self.drive = subsystems.drivetrain.Drivetrain(self)

		# Driverstation
		self.driverstation = wpilib.DriverStation.getInstance()

		# Power Distribution Panel
		self.pdp = wpilib.PowerDistributionPanel()

		# Robot Components -- subsystems
		self.hatch = subsystems.hatch.Hatch(self)
		self.cargo = subsystems.cargo.Cargo(self)
		self.climber = subsystems.climber.Climber(self)

		# Limelight camera
		self.limelight = subsystems.limelight.Limelight(self)

		# Arduino / line sensors
		self.arduino = subsystems.arduino.Arduino(self)

		# Gyro
		# self.gyro = wpilib.ADXRS450_Gyro()

		# Ultrasonics
		self.ultrasonic_front = wpilib.AnalogInput(const.AIN_ULTRASONIC_FRONT)
		self.ultrasonic_rear = wpilib.AnalogInput(const.AIN_ULTRASONIC_REAR)

		# Operator Input
		self.oi = oi.OI(self)

		# Encoders -- change after encoders are decided and added
		self.use_enc_correction = False

		self.drive_encoder_left = wpilib.Encoder(const.DIO_DRIVE_ENC_LEFT_1, const.DIO_DRIVE_ENC_LEFT_2, reverseDirection = const.DRIVE_ENCODER_LEFT_REVERSED)
		self.drive_encoder_right = wpilib.Encoder(const.DIO_DRIVE_ENC_RIGHT_1, const.DIO_DRIVE_ENC_RIGHT_2, reverseDirection = const.DRIVE_ENCODER_RIGHT_REVERSED)

		self.drive_encoder_left.setDistancePerPulse(1 / const.DRIVE_TICKS_PER_FOOT)
		self.drive_encoder_right.setDistancePerPulse(1 / const.DRIVE_TICKS_PER_FOOT)

		self.climber.front_axle_motor.setSelectedSensorPosition(0, 0, 10)
		self.climber.back_axle_motor.setSelectedSensorPosition(0, 0, 10)

		# Pressure Sensor (200 psi)
		# self.pressure_sensor = wpilib.AnalogInput(const.AIN_PRESSURE_SENSOR)

		# Timer for pressure sensor's running average
		# self._pressure_samples = []
		# self._last_pressure_value = 0.0
		# self.pressure_timer = wpilib.Timer()
		# self.pressure_timer.start()
		# self.pressure_timer_delay = 1.0		# times per second

		# Time robot object was created
		# self.start_time = time.time()

		## Scheduler ##
		self.scheduler = wpilib.command.Scheduler.getInstance()

		### LOGGING ###
		# Timers for NetworkTables update so we don't use too much bandwidth
		self.log_timer = wpilib.Timer()
		self.log_timer.start()
		self.log_timer_delay = 0.25		# 4 times/second

		# NetworkTables
		self.nt_robot = networktables.NetworkTables.getTable('Robot')

		# cProfile object
		if const.CPROFILE_ENABLED:
			self.profiler = cProfile.Profile( )
		else:
			self.profiler = None

	### DISABLED ###

	def disabledInit(self):
		self.scheduler.removeAll()

		# self.limelight.table.putNumber('stream',2)		# 0 = side-by-side, 1 = PIP Main, 2 = PIP Secondary
		# self.limelight.set_driver_mode(const.DRIVER_CAMERA_MODE_DEFAULT)

		if const.CPROFILE_ENABLED:
			self.profiler.disable( )
			if os.path.exists('/var/tmp/profile.pstat'):
				os.remove('/var/tmp/profile.pstat')
			self.profiler.dump_stats( '/var/tmp/profile.pstat' )

	def disabledPeriodic(self):
		pass
		self.log()


	### AUTONOMOUS ###

	def autonomousInit(self):
		pass

	def autonomousPeriodic(self):
		pass


	### TELEOPERATED ###

	def teleopInit(self):
		wpilib.LiveWindow.disableAllTelemetry()
		self.limelight.set_driver_mode(const.DRIVER_CAMERA_MODE_ENABLED)

		# Removes any leftover commands from the scheduler
		self.scheduler.removeAll()

		self.climber.stop_back_axle()
		self.climber.stop_front_axle()
		self.climber.stop_drive_front_axle()

		self.cargo.stop_arm()

		# Reset all robot parts
		#self.gyro.reset()

		# Drive encoders
		self.drive_encoder_left.reset()
		self.drive_encoder_right.reset()

		if const.CPROFILE_ENABLED:
			self.profiler.enable( )


	def teleopPeriodic(self):
		# if self.driverstation.getMatchTime() < 30:
		# 	self.arduino.set_led_state('c')

		self.scheduler.run()
		self.log()


	### MISC ###

	def get_pressure(self):
		"""
		Calculate a running average of pressure values.  The sensor seems to jitter its values
		a lot, so this should smooth it out and make the SD display more readable.
		"""

		# voltage_pressure = self.pressure_sensor.getVoltage()
		# new_value = (250 * voltage_pressure / 5) - 25

		# self._pressure_samples.append(new_value)

		# if not self.pressure_timer.hasPeriodPassed(self.pressure_timer_delay):
		# 	return self._last_pressure_value

		# # Calculate new running average
		# new_avg = sum(self._pressure_samples) / len(self._pressure_samples)

		# self._pressure_samples = [ ]
		# self._last_pressure_value = new_avg

		#return new_avg

	def log(self):
		"""
		Logs some info to shuffleboard, and standard output
		"""

		# Only every 1/10 second or so to avoid flooding networktables
		if not self.log_timer.running or not self.log_timer.hasPeriodPassed(self.log_timer_delay):
			return

		# self.nt_robot.putString('Pressure', '{0:.2f}'.format(self.get_pressure()))
		#self.nt_robot.putString('Ultrasonic', '{0:.2f}'.format(self.ultrasonic.getVoltage( ) / ( 5 / 512 )))
		self.drive.log()
		self.hatch.log()
		self.cargo.log()
		self.climber.log()
		self.limelight.log()
		self.arduino.log()

### MAIN ###

if __name__ == "__main__":
	wpilib.run(Robot)