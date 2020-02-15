#!/usr/bin/python

import argparse
import curses
import numpy as np
import numpy.random as rand

from curses import wrapper


def valid(shape, c):
    return (c >= 0).all() and (c < shape).all()


def putchar(scr, pos, color, char):
    scr.addstr(pos[0], pos[1], '')
    scr.addstr(char, curses.color_pair(color))


def printmap(scr, shape):
    scr.clear()
    for i in range(shape[0]):
        for j in range(shape[1]):
            pos = np.array([i, j])
            putchar(scr, pos, 6, 'z')


def balloon(scr, shape, pos, radius, color):
    for i in range(shape[0]):
        for j in range(shape[1]):
            di = i - pos[0]
            dj = j - pos[1]
            if di * di + dj * dj <= radius * radius:
                putchar(scr, [i,j], color, '*')
                

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
    pos = shape // 2
    board = np.zeros(shape, dtype=int)
    printmap(scr, shape)

    dirs = {curses.KEY_DOWN: [1, 0],
            curses.KEY_UP: [-1, 0],
            curses.KEY_LEFT: [0, -1],
            curses.KEY_RIGHT: [0, 1]}

    radius = 0
    color = 1
    while True:
        key = scr.getch()
        if key in colormap:
            if color != colormap[key]:
                radius = 0
                color = colormap[key]
                putchar(scr, pos, color, '.')
                continue
            radius += 1
            balloon(scr, shape, pos, radius, color)
            continue
        radius = 0
        if key == 27:
            break
        if key not in dirs:
            continue
        delta = np.array(dirs[key])
    
        new_pos = pos + delta
        if not valid(shape, new_pos):
            continue
    
        putchar(scr, pos, color, ' ')
        pos = new_pos
        putchar(scr, pos, color, '.')

wrapper(main)

