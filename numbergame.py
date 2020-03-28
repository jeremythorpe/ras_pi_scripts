
import argparse
import sys
import os
import numpy as np
import curses
from curses import wrapper

def main(_):
  parser = argparse.ArgumentParser(description='Number game.')
  parser.add_argument('-n', type=int, default=6)
  args = parser.parse_args()

  blank = '\n\n\n\n\n\n\n     '
  code = ''
  scr = curses.initscr()
  curses.cbreak()
  curses.noecho()
  scr.keypad(True)
  curses.raw()
  curses.curs_set(False)
  curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
  curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
  curses.init_pair(3, curses.COLOR_BLUE, curses.COLOR_BLACK)

  turn = 0
  while True:
    turn += 1
    turn %= 4

    player_turn = (turn % 2) == 1
    if player_turn:
      ops = ['+','-']
      op = ops[turn // 2]
      operands = np.random.randint(args.n, size=2)
      if args.n > 9:
        operands *= 10 ** np.random.randint(args.n - 9, size=2)
      problem = '\n\n\n\n\n\n     {} {} {} = '.format(operands[0], op, operands[1])
      answer = ''
      solution = operands[0] + operands[1] if op == '+' else operands[0] - operands[1]

    else:
      op = '*'
      operands = np.random.randint(args.n, size=2)
      if args.n > 9:
        operands *= 10 ** np.random.randint(args.n - 9, size=2)
      if args.n > 9:
        operands *= 10 ** np.random.randint(args.n - 9, size=2)
      solution = operands[0] * operands[1]
      problem = '\n\n\n\n\n\n     {} {} {} = {}'.format(operands[0], op, operands[1], solution)

    while True:
      scr.clear()
      if player_turn:
        scr.addstr(problem)
        scr.addstr(answer, curses.color_pair(2))
      else:
        scr.addstr(problem, curses.color_pair(1))
      x = scr.getch()
      if x < 128 or x == 263:
        if x == 263:
          answer = answer[:-1]
        elif x >= 48 and x < 58 or x == 45:
          #if player_turn:
          answer += str(chr(x))
        elif x == 10:
          if player_turn and answer and int(answer) != solution:
            turn += 1
          break
        elif x == 27:
          return

wrapper(main)

