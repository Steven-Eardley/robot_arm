#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import threading
import curses

halt = False
input_queue = []

def stop():
    print("stopped!")


def movement(fn):
    def decorated_view(*args, **kwargs):
        try:
            halt = False
            fn(*args, **kwargs)
        except KeyboardInterrupt:
            stop()
            raise
    return decorated_view


@movement
def slow():
    for i in range(0, 200):
        print(i)
        time.sleep(1)
        if halt:
            return


@movement
def slow2():
    for i in range(999, 200, -1):
        print(i)
        time.sleep(1)
        if halt:
            return


def input_thread(q, screen):
    while True:
        q.append(screen.getkey())
        time.sleep(0.1)


fn_map = {
    'w': slow,
    's': slow2,
    'a': None,
    'd': None,
    'q': None,
    'e': None,
    'x': stop,
}

def main(screen):
    #screen.nodelay(True)
    curses.echo()
    t = threading.Thread(name='arm_imput', target=input_thread, args=(input_queue, screen,))
    t.setDaemon(True)
    t.start()

    while True:
        try:
            k = input_queue.pop()
            if k in fn_map:
                halt = True            # On new valid input, stop current action
                time.sleep(2)
            fn_map[k]()
            print(f"POPPED {k}")
        except (IndexError, KeyError):
            # Wait for input
            time.sleep(0.1)


if __name__ == '__main__':
    curses.wrapper(main)
