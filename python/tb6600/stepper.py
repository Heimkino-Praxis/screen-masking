import RPi.GPIO as GPIO
import time
import os

GPIO.setmode(GPIO.BOARD)


# TB6600 Stepper Driver
DIR = 33
PUL = 35
ENA = 37

DIR_Leave = GPIO.HIGH
DIR_Revert = GPIO.LOW

ENA_Locked = GPIO.LOW
ENA_Released = GPIO.HIGH

GPIO.setwarnings(False)
GPIO.setup(DIR, GPIO.OUT)
GPIO.setup(PUL, GPIO.OUT)
GPIO.setup(ENA, GPIO.OUT)


# Relay module for driver power
POWER = 11

GPIO.setup(POWER, GPIO.OUT)


# Motor Setup
STEP_ANGLE = 0.9 # degree
RAMP_LENGTH = 600 # steps
MIN_RPM = 250
MAX_RPM = 800

# max steps the motor should ever turn (min = 0)
MAX_STEPS = 10000 # = 20 cm


stepsPerRevolution = 360 / STEP_ANGLE # 400

minFrequency = 1 / (MAX_RPM / 60 * stepsPerRevolution) # fastest
maxFrequency = 1 / (MIN_RPM / 60 * stepsPerRevolution) # slowest

rampSlope = (maxFrequency - minFrequency) / RAMP_LENGTH


class MaskException(Exception):
	pass


def getCurrentPosition ():

	try:
		f = open(".position", "r")
		steps = int(f.read())
		f.close()
		return steps
	except IOError:
		return 0


def setCurrentPosition (steps):

	f = open(".position", "w+");
	f.write(str(steps))
	f.close()


def getBusy ():

	try:
		f = open(".busy", "r")
		busy = int(f.read())
		f.close()

		if (busy == 1):
			return True
		else:
			return False

	except IOError:
		return False


def setBusy (busy):

	if (busy == True):
		f = open(".busy", "w+");
		f.write("1")
		f.close()
	else:
		try:
			os.remove(".busy")
		except IOError:
			print("Busy file could not be removed")


def moveTo (position):

	if (getBusy()):
		raise MaskException("Device is busy")

	if (position < 0):
		position = 0
	if (position > MAX_STEPS):
		position = MAX_STEPS

	currentPosition = getCurrentPosition()
	steps = position - currentPosition

	return moveBy(steps)


def moveBy (steps):

	if (getBusy()):
		raise MaskException("Device is busy")

	setPower(1)
	setLock(1)

	setBusy(True)

	currentFreqency = maxFrequency
	currentPosition = getCurrentPosition()

	# there are some security shutdowns, but pre-calculate the real step count anyway
	targetPosition = currentPosition + steps
	if (targetPosition > MAX_STEPS):
		steps = MAX_STEPS - currentPosition
	if (targetPosition < 0):
		steps = currentPosition * -1

	for i in range(abs(steps)):

		# stop when motor leaves the valid area upwards
		if (steps >= 0 and currentPosition >= MAX_STEPS):
			setLock(0)
			setCurrentPosition(currentPosition)
			setBusy(False)
			return currentPosition

		# stop when motor leaves the valid area downwards
		if (steps < 0 and currentPosition <= 0):
			setLock(0)
			setCurrentPosition(currentPosition)
			setBusy(False)
			return currentPosition

		# set direction
		if (steps < 0):
			GPIO.output(DIR, DIR_Revert)
		else:
			GPIO.output(DIR, DIR_Leave)

		# perform step
		GPIO.output(PUL, GPIO.HIGH)
		time.sleep(currentFreqency / 2)
		
		GPIO.output(PUL, GPIO.LOW)
		time.sleep(currentFreqency / 2)

		if (steps < 0):
			currentPosition -= 1
		else:
			currentPosition += 1

		# apply ramp slope
		if (abs(steps) > 2 * RAMP_LENGTH):
			if (i < RAMP_LENGTH):
				currentFreqency -= rampSlope
			else:
				if (i > abs(steps) - RAMP_LENGTH):
					currentFreqency += rampSlope
		else:
			if (i < abs(steps) / 2):
				currentFreqency -= rampSlope
			else:
				currentFreqency += rampSlope

		#print(currentFreqency)

	setCurrentPosition(currentPosition)
	
	setBusy(False)

	setLock(0)
	return currentPosition


def forceBy (steps):

	if (getBusy()):
		raise MaskException("Device is busy")

	setPower(1)
	setLock(1)

	setBusy(True)

	for i in range(abs(steps)):

		# set direction
		if (steps < 0):
			GPIO.output(DIR, DIR_Revert)
		else:
			GPIO.output(DIR, DIR_Leave)

		# perform step
		GPIO.output(PUL, GPIO.HIGH)
		time.sleep(maxFrequency / 2)
		
		GPIO.output(PUL, GPIO.LOW)
		time.sleep(maxFrequency / 2)

	setBusy(False)

	setLock(0)


def calibrate ():

	if (getBusy()):
		raise MaskException("Device is busy")

	setCurrentPosition(0)
	setLock(0)


def setLock (value):

	if (getBusy()):
		raise MaskException("Device is busy")

	if (value > 0):
		GPIO.output(ENA, ENA_Locked)
	else:
		time.sleep(0.2) # hold for a short time without signals, to instantly stop the motor
		GPIO.output(ENA, ENA_Released)	


def getPower ():

	power = GPIO.input(POWER)

	if (power == 0):
		return 1
	else:
		return 0


def setPower (value):

	if (getBusy()):
		raise MaskException("Device is busy")

	if (value > 0):
		GPIO.output(POWER, GPIO.LOW)
		time.sleep(0.2) # wait for driver to boot (it's pretty fast, but losing steps would be a pain)
	else:
		GPIO.output(POWER, GPIO.HIGH)
