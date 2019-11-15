import stepper
import time


print("motor released ...")
stepper.release()

time.sleep(1)
print("... 3")
time.sleep(1)
print("... 2")
time.sleep(1)
print("... 1")
time.sleep(1)


print("motor locked ...")
stepper.lock()

time.sleep(1)
print("... 3")
time.sleep(1)
print("... 2")
time.sleep(1)
print("... 1")
time.sleep(1)


print("moving to position 200")
stepper.moveTo(200)
time.sleep(1)

print("moving by another 200 steps")
stepper.moveBy(200)
time.sleep(1)

print("requesting position")
position = stepper.getCurrentPosition()
print("position: " + str(position))
time.sleep(1)

print("forcing by -200 steps")
stepper.forceBy(-200)
time.sleep(1)

print("forcing by 200 steps")
stepper.forceBy(200)
time.sleep(1)

print("moving by -200 steps")
stepper.moveBy(-200)
time.sleep(1)

print("moving to position 0")
stepper.moveTo(0)
time.sleep(1)

print("done")
