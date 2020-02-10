

import argparse
import curses
import numpy as np
import numpy.random as rand

from curses import wrapper


diffs = np.array([[0,1],[0,-1],[1,0],[-1,0]])


def valid(shape, c):
  return (c >= 0).all() and (c < shape).all()


def putchar(scr, pos, color, char):
  scr.addstr(pos[0], pos[1], '')
  scr.addstr(char, curses.color_pair(color))


def move(scr, shape, pos, color, colormap):
  key = scr.getch()
  dirs = {curses.KEY_DOWN: [1, 0],
          curses.KEY_UP: [-1, 0],
          curses.KEY_LEFT: [0, -1],
          curses.KEY_RIGHT: [0, 1]}
  if key in colormap:
    color[0] = colormap[key]
    putchar(scr, pos[0], color[0], '.')
    return
  if key == 27:
    return True
  if key not in dirs:
    return
  delta = np.array(dirs[key])

  new_pos = pos[0] + delta
  if not valid(shape, new_pos):
    return

  putchar(scr, pos[0], color[0], ' ')
  pos[0] = new_pos
  putchar(scr, pos[0], color[0], '.')
  return


def printmap(scr, shape):
  scr.clear()
  for i in range(shape[0]):
    for j in range(shape[1]):
      pos = np.array([i, j])
      putchar(scr, pos, 6, 'z')


def main(_):
  parser = argparse.ArgumentParser(description='Fun maze game.')
  parser.add_argument('-t', type=int, default=10)
  parser.add_argument('-w', type=int, default=20)
  args = parser.parse_args()

  scr = curses.initscr()
  scr.keypad(True)
  curses.raw()
  curses.curs_set(False)
  colormap = {
    ord('k'): curses.COLOR_BLACK,
    ord('r'): curses.COLOR_RED,
    ord('g'): curses.COLOR_GREEN,
    ord('y'): curses.COLOR_YELLOW,
    ord('b'): curses.COLOR_BLUE,
    ord('m'): curses.COLOR_MAGENTA,
    ord('c'): curses.COLOR_CYAN,
    ord('w'): curses.COLOR_WHITE,
  }
  idx = 1
  for key, value in colormap.items():
    if key == ord('k'):
      curses.init_pair(idx, curses.COLOR_WHITE, value)
    else:
      curses.init_pair(idx, curses.COLOR_BLACK, value)
    colormap[key] = idx
    idx += 1

  shape = np.array([args.t, args.w])
  pos = [np.array([5,5])]
  printmap(scr, shape)

  color = [1]
  while True:
    if move(scr, shape, pos, color, colormap):
      break

wrapper(main)

