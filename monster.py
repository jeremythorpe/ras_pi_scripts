
import numpy as np
import curses
from curses import wrapper

def makemap():
  z = np.random.rand(14, 50)
  map = np.floor(z + .1) + np.floor(z + .1)
  map[0] = 1
  map[-1] = 1
  map[:,0] = 1
  map[:,-1] = 1
  map[0, map.shape[1] // 2] = 0
  map[1, map.shape[1] // 2] = 3
  return map
  
def get_pos(map):
  for i in range(len(map)):
    for j in range(len(map[i])):
      if map[i, j] == 3:
        return np.array([i, j])
  return None

def printmap(scr, map):
  s = ''
  rep = {0: '.',
         1: '*',
         2: 'M',
         3: '#'}
  lines = []
  for i in range(map.shape[0]):
    lines.append(''.join([rep[m] for m in map[i]]))
  scr.clear()
  for line in lines:
    scr.addstr(line)

def valid(map, pos):
  if pos[0] < 0:
    return False
  if pos[0] >= map.shape[0]:
    return False
  if pos[1] < 0:
    return False
  if pos[1] >= map.shape[1]:
    return False
  return True

def move(scr, map):
  key = scr.getch()
  dirs = {curses.KEY_DOWN: [1, 0],
          curses.KEY_UP: [-1, 0],
          curses.KEY_LEFT: [0, -1],
          curses.KEY_RIGHT: [0, 1]}
  if key == 27:
    return True
  pos = get_pos(map)
  if pos is None:
    return
  if key == 98:
    for key, value in dirs.items():
      delta = np.array(dirs[key])
      new_pos = pos + delta
      if valid(map, new_pos):
        map[new_pos[0], new_pos[1]] = 0
    printmap(scr, map)
    return
  if key not in dirs:
    return
  delta = np.array(dirs[key])
  new_pos = pos + delta
  if not valid(map, new_pos):
    return
  if map[new_pos[0], new_pos[1]] == 1:
    return
  if new_pos is not None:
    map[pos[0], pos[1]] = 0
    scr.addch(pos[0], pos[1], '.')
    map[new_pos[0], new_pos[1]] += 3
    map[new_pos[0], new_pos[1]] %= 4
    scr.addch(new_pos[0], new_pos[1], '#')
    return

def main(_):
  scr = curses.initscr()
  scr.keypad(True)
  curses.raw()
  curses.curs_set(False)
  map = makemap()
  printmap(scr, map)
  while True:
    if move(scr, map):
      break

wrapper(main)

