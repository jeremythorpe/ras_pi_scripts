

import argparse
import curses
import numpy as np
import numpy.random as rand

from curses import wrapper


win = False

diffs = np.array([[0,1],[0,-1],[1,0],[-1,0]])

def valid(maze, c):
  return (c >= 0).all() and (c < maze.shape).all()

def fill_two(maze, c):
  if maze[c[0], c[1]]:
    return
  maze[c[0], c[1]] = 2
  for d in range(4):
    cnext = c + diffs[d, :]
    if valid(maze, cnext):
      fill_two(maze, cnext)

def reachable(maze, c):
  maze_copy = maze.copy()
  maze_copy *= maze_copy < 3
  fill_two(maze_copy, c)
  return np.sum(np.floor(maze_copy / 2))

def open_adjacent(maze, c):
  a = 0
  for d in range(4):
    cnext = c + diffs[d, :]
    if valid(maze, cnext) and maze[cnext[0], cnext[1]] == 0:
      a += 1
  return a

def make_maze(h, w):
  maze = np.zeros([h, w])
  while True:
    start = (rand.random([2]) * maze.shape).astype(np.int)
    if (start == 0).any():
      break
    if (start + 1 == maze.shape).any():
      break
  end = maze.shape - start - 1
  maze[start[0], start[1]] = 3
  maze[end[0], end[1]] = 4
  r = np.prod(maze.shape)
  for i in range(500):
    c = (rand.random([2]) * maze.shape).astype(np.int)
    if maze[c[0], c[1]] != 0:
      continue
    if open_adjacent(maze, c) < 2:
      continue
    maze[c[0], c[1]] = 1
    if reachable(maze, start) < r - 1:
      maze[c[0], c[1]] = 0
    else:
      r -= 1
  return maze

def get_pos(maze):
  for i in range(len(maze)):
    for j in range(len(maze[i])):
      if maze[i, j] == 3:
        return np.array([i, j])
  return None

def putchar(scr, pos, value):
  value = int(value)
  rep = {0: ' ',
         1: '*',
         2: 'o',
         3: '#',
         4: '$'}
  scr.addstr(pos[0], pos[1], '')
  scr.addstr(rep[value], curses.color_pair(value))

def printmap(scr, maze):
  scr.clear()
  for i in range(maze.shape[0]):
    for j in range(maze.shape[1]):
      m = maze[i][j]
      pos = np.array([i, j])
      putchar(scr, pos, m)

def valid(maze, pos):
  if pos[0] < 0:
    return False
  if pos[0] >= maze.shape[0]:
    return False
  if pos[1] < 0:
    return False
  if pos[1] >= maze.shape[1]:
    return False
  return True

def move(scr, maze):
  key = scr.getch()
  pos = get_pos(maze)
  dirs = {curses.KEY_DOWN: [1, 0],
          curses.KEY_UP: [-1, 0],
          curses.KEY_LEFT: [0, -1],
          curses.KEY_RIGHT: [0, 1]}
  if key == 27:
    return True
  if key not in dirs:
    return
  pos = get_pos(maze)
  delta = np.array(dirs[key])
  new_pos = pos + delta
  if not valid(maze, new_pos):
    return
  if maze[new_pos[0], new_pos[1]] == 1:
    return
  if maze[new_pos[0], new_pos[1]] == 4:
    global win
    win = True
    return True
  if new_pos is not None:
    maze[pos[0], pos[1]] = 0
    putchar(scr, pos, 0)
    maze[new_pos[0], new_pos[1]] = 3
    putchar(scr, new_pos, 3)
    return

def main(_):
  parser = argparse.ArgumentParser(description='Fun maze game.')
  parser.add_argument('-t', type=int, default=10)
  parser.add_argument('-w', type=int, default=20)
  args = parser.parse_args()

  scr = curses.initscr()
  scr.keypad(True)
  curses.raw()
  curses.curs_set(False)
  curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_MAGENTA)
  curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
  curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLUE)
  curses.init_pair(4, curses.COLOR_WHITE, curses.COLOR_CYAN)
  maze = make_maze(args.t, args.w)
  printmap(scr, maze)
  while True:
    if move(scr, maze):
      break
  scr.clear()
  scr.refresh()
  if win:
    print("You win!")

wrapper(main)

