
import time
import numpy as np

from adafruit_motor import stepper
from adafruit_motorkit import MotorKit

kit = MotorKit()

rotation = np.array([[0., 1.], [-1, 0]])

def normalize(x):
  return x / np.sqrt(np.sum(np.square(x)))

def move_by(stepperN, delta):
  if delta:
    direction = stepper.FORWARD if delta > 0 else stepper.BACKWARD
    stepperN.onestep(direction=direction, style=stepper.DOUBLE)
    time.sleep(.01)

pos = np.array([0., 1.])
for i in range(1000):
  direction = normalize(pos) + np.matmul(rotation, pos)
  direction = normalize(direction)
  new_pos = pos + direction
  delta_quant = np.round(new_pos) - np.round(pos)
  move_by(kit.stepper1, delta_quant[0])
  move_by(kit.stepper2, delta_quant[1])

  pos = new_pos

kit.stepper1.release()
kit.stepper2.release()
