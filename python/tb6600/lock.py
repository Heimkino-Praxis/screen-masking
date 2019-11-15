import stepper
import sys


if (len(sys.argv) != 2):
	print("missing parameter: 0|1");
	sys.exit();


value = int(sys.argv[1])

stepper.setLock(value)

if (value > 0):
	print("motor locked")
else:
	print("motor released")
