# -*- coding: utf-8 -*-

# Code borrowed from pyte example.
"""
    nanoterm
    ~~~~~~~~

    An example showing how to feed :class:`~pyte.streams.Stream` from
    a running terminal app.

    :copyright: (c) 2015 by pyte authors and contributors,
                see AUTHORS for details.
    :license: LGPL, see LICENSE for more details.
"""

from __future__ import print_function, unicode_literals

import os
import pty
import select
import signal
import sys
import time

import pyte

# Terminal dimensions in column-row order.
sdims = (80, 24)

# Arrow keys
up = "\033[A"
down = "\033[B"
right = "\033[C"
left = "\033[D"

# Given a file to send to, and strings representing
# keystrokes to send, send the keystrokes.
def send(f, *keys):
    os.write(f, bytes(''.join(keys), encoding="ascii"))

# Generate a desired screen with indicated characters at the
# indicated coordinates, and spaces everywhere else.
class TestScreen(object):
    def __init__(self, name, nonblank):
        self.name = name
        cols, rows = sdims
        self.screen = [[
            nonblank[(r, c)] if (r, c) in nonblank else ' '
            for c in range(cols)] for r in range(rows)]

    def matches(self, scr):
        cols, rows = sdims
        for r in range(rows):
            for c in range(cols):
                if self.screen[r][c] != scr[r][c]:
                    print("mismatch", r, c, self.screen[r][c], scr[r][c])
                    return False
        return True

    def test(self, testname, scr):
        if not self.matches(scr):
            print(f"{testname} ({self.name}) mismatched")
            print(self)
            print("---")
            print(*scr, sep="\n")
            exit(1)

    def __str__(self):
        return '\n'.join([''.join([c for c in row]) for row in self.screen])

flasher_vertical = TestScreen("flasher vertical", {
    (1, 1): 'x',
    (2, 1): 'x',
    (3, 1): 'x',
})

flasher_horizontal = TestScreen("flasher horizontal", {
    (2, 0): 'x',
    (2, 1): 'x',
    (2, 2): 'x',
})

def flasher_test(state, f, scr):
    print(f"state {state}")
    if state == 0:
        send(f, right, down, "X", down, "X", down, "X")
        time.sleep(0.05)
        return 1
    if state == 1:
        flasher_vertical.test("vertical 1", scr)
        send(f, "p")
        time.sleep(0.1)
        return 2
    if state == 2:
        flasher_horizontal.test("horizontal", scr)
        time.sleep(0.1)
        return 3
    if state == 3:
        flasher_vertical.test("vertical 2", scr)
        return None
    assert False

if len(sys.argv) <= 1:
    sys.exit("usage: %prog% command [args]")

screen = pyte.Screen(*sdims)
stream = pyte.ByteStream(screen)

p_pid, master_fd = pty.fork()
if p_pid == 0:  # Child.
    os.execvpe(sys.argv[1], sys.argv[1:],
               env=dict(TERM="linux", COLUMNS="80", LINES="24"))

test_state = 0
while test_state is not None:
    try:
        read_list, _write_list, except_list = select.select(
            [master_fd], [], [master_fd], 1)
    except KeyboardInterrupt:
        # Stop right now!
        break
    else:
        if except_list:
            print("exception")
            exit(1)
        elif read_list:
            data = os.read(read_list[0], 1024)
            if not data:
                break
            stream.feed(data)
            test_state = flasher_test(test_state, master_fd, screen.display)

exit(0)
