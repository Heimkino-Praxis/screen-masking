import stepper
import sys


if (len(sys.argv) != 2):
	print("missing parameter: 0|1");
	sys.exit();


value = int(sys.argv[1])

stepper.setLock(0)
stepper.setPower(value)

if (value > 0):
	print("power on")
else:
	print("power off")
