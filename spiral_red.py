
import time
import numpy as np

from gpiozero import LED

leds = [LED(i) for i in [21, 23, 24, 25]]

rotation = np.array([[0., 1.], [-1, 0]])

def normalize(x):
  return x / np.sqrt(np.sum(np.square(x)))

pos_to_state = [[1, 1, 0, 0],
                [0, 0, 1, 1],
                [1, 0, 0, 1],
                [0, 1, 1, 0]]
pos_to_state = [[1, 1, 1, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 1, 1, 1, 0],
                [1, 0, 0, 0, 0, 0, 1, 1],
                [0, 0, 1, 1, 1, 0, 0, 0]]

def move_to(pos):
  for i in range(4):
    if pos_to_state[i][pos % 8]:
      leds[i].on()
    else:
      leds[i].off()
  time.sleep(.1)

pos = np.array([0., 1.])
for i in range(300):
  direction = normalize(pos) + np.matmul(rotation, pos)
  direction = normalize(direction)
  pos = pos + direction
  move_to(int(np.round(pos[0])))
