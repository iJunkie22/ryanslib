#!/usr/bin/env python2.7
import subprocess
import string

A_S_COLOR_MAX = 65535
A_S_COLOR_MIN = 0

myscript = \
"""
tell application "Terminal"
    set output to (choose color)
    return ((first text item of output) as text) & "," & ((second text item of output) as text) & "," & ((third text item of output) as text)
end tell
"""


def as_color_to_hex(as_color_str):
    as_clr_int = int(as_color_str)
    clr_in = (as_clr_int * 255) / A_S_COLOR_MAX
    return ''.join([string.hexdigits[0:16][x] for x in divmod(clr_in, 16)])


def get_a_color():
    p1 = subprocess.Popen(['/usr/bin/osascript', '-'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)
    stdo, stderr = p1.communicate(myscript)
    hex_str = ''.join([as_color_to_hex(as_color_str) for as_color_str in stdo.split(',')])
    return '#' + hex_str


if __name__ == '__main__':
    result = get_a_color()
    print result
