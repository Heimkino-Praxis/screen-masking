import stepper
import sys


if (len(sys.argv) != 2):
	print("missing parameter: steps");
	sys.exit();


steps = int(sys.argv[1])
#print("steps: " + str(steps))

currentPosition = stepper.moveTo(steps)
print(currentPosition)
