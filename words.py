
import numpy as np
import curses
from curses import wrapper

import getcode

def main(_):
  blank = '\n\n\n\n\n\n\n     '
  with open ('words', 'r') as f:
    d = f.read()
  words = {word: True for word in d.split('\n')}
  prefixes = {}
  for word in words:
    for i in range(1, len(word)):
      prefixes[word[:i]] = True
  code = ''
  scr = curses.initscr()
  scr.keypad(True)
  curses.raw()
  curses.curs_set(False)
  getcode.getcode(scr)
  curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
  curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
  curses.init_pair(3, curses.COLOR_BLUE, curses.COLOR_BLACK)
  while True:
    x = scr.getch()
    if x < 128:
      if x == 9:
        goodwords = {word: True for word in words if word.startswith(code)}
        if goodwords:
          code = goodwords.keys()[0]
      else:
        code += str(chr(x))
        if not code in prefixes:
          code = code[:-1]
      scr.clear()
      if code in words:
        scr.addstr(blank + code, curses.color_pair(1))
      elif code in prefixes:
        scr.addstr(blank + code)
      elif code.isdigit():
        scr.addstr(blank + code, curses.color_pair(3))
      else:
        scr.addstr(blank + code, curses.color_pair(2))
    if x == 10:
      if len(code[:-1]) >= 4:
        words[code[:-1]] = True
      code = ''
      scr.clear()
    if x == 27:
      return

wrapper(main)

