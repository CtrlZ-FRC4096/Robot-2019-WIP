"""
EXPERIMENTAL!  Do not use!  See Adam

Ctrl-Z FRC Team 4096
FIRST Robotics Competition 2018
Code for robot "Atla-Z"
contact@team4096.org
"""

import wpilib

# Xbox Controller
# Buttons
BTN_A					= wpilib.XboxController.Button.kA
BTN_B					= wpilib.XboxController.Button.kB
BTN_X					= wpilib.XboxController.Button.kX
BTN_Y					= wpilib.XboxController.Button.kY
BTN_BACK 				= wpilib.XboxController.Button.kBack
BTN_START 				= wpilib.XboxController.Button.kStart

LEFT					= wpilib.XboxController.Hand.kLeft
RIGHT					= wpilib.XboxController.Hand.kRight

# Axes
AXIS_LEFT_X    		    = 0
AXIS_LEFT_Y				= 1
AXIS_RIGHT_X			= 4
AXIS_RIGHT_Y			= 5
# XBOX_BTN_LEFT_TRIGGER	= 2
# XBOX_BTN_RIGHT_TRIGGER	= 3

# # D-Pad
# JOY_POV_NONE			= -1
# JOY_POV_UP				= 0
# JOY_POV_UP_RIGHT		= 45
# JOY_POV_RIGHT			= 90
# JOY_POV_DOWN_RIGHT		= 135
# JOY_POV_DOWN			= 180
# JOY_POV_DOWN_LEFT		= 225
# JOY_POV_LEFT			= 270
# JOY_POV_UP_LEFT			= 315

# INVERT_XBOX_LEFT_X		= True
# INVERT_XBOX_LEFT_Y		= False
# INVERT_XBOX_RIGHT_X		= True
# INVERT_XBOX_RIGHT_Y		= True



class Xbox_Controller( wpilib.XboxController ):
	'''
	Allows usage of an Xbox controller, with sensible names for Xbox
	specific buttons and axes.

	Mapping based on http://www.team358.org/files/programming/ControlSystem2015-2019/images/XBoxControlMapping.jpg
	'''

	def getLeftTrigger(self):
		'''
		Get the left stick trigger

		:returns: -1 to 1
		:rtype: float
		'''
		return self.ds.getStickAxis(self.port, 2)

	def getRightTrigger(self):
		'''
		Get the right stick trigger

		:returns: -1 to 1
		:rtype: float
		'''
		return self.ds.getStickAxis(self.port, 3)

	def getAxis(self, axis):
		'''
		For the current joystick, return the axis determined by the
		argument.

		This is for cases where the joystick axis is returned programmatically,
		otherwise one of the previous functions would be preferable (for
		example :func:`getX`).

		:param axis: The axis to read.
		:type axis: :class:`Joystick.AxisType`
		:returns: The value of the axis.
		:rtype: float
		'''

		if axis == XBOX_AXIS_LEFT_X:
			return self.getX( self.Hand.kLeft )
		elif axis == XBOX_AXIS_LEFT_Y:
			return self.getY( self.Hand.kLeft )
		elif axis == XBOX_AXIS_RIGHT_X:
			return self.getX( self.Hand.kRight )
		elif axis == XBOX_AXIS_RIGHT_Y:
			return self.getY( self.Hand.kRight )
		elif axis == XBOX_BTN_LEFT_TRIGGER:
			return self.getLeftTrigger()
		elif axis == XBOX_BTN_RIGHT_TRIGGER:
			return self.getRightTrigger()

		else:
			raise ValueError("Invalid axis specified! Must be one of wpilib.Joystick.AxisType, or use getRawAxis instead")