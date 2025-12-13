# Input handler

import sys
import os

if sys.platform == "win32":
    import msvcrt
else:
    import termios
    import tty

# nonstandard keys
KEY_UP = "up"
KEY_DOWN = "down"
KEY_RIGHT = "right"
KEY_LEFT = "left"
KEY_ENTER = "enter"
KEY_ESC = "esc"
KEY_BACKSPACE = "backspace"

def read_key():
    if sys.platform == "win32":
        ch = msvcrt.getch()
        if ch in (b"\xe0", b"\x00"):
            ch2 = msvcrt.getch()
            if ch2 == b"H":
                return KEY_UP
            elif ch2 == b"P":
                return KEY_DOWN
            elif ch2 == b"M":
                return KEY_RIGHT
            elif ch2 == b"K":
                return KEY_LEFT
        elif ch == b"\r":
            return KEY_ENTER
        elif ch == b"\x1b":
            return KEY_ESC
        elif ch == b"\x08":
            return KEY_BACKSPACE
        elif ch.isascii() and ch.isprintable():
            return ch.decode("utf-8").lower()
        else:
            return ch.decode("utf-8", errors = "ignore")
        
    else:
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = os.read(fd, 1).decode("utf-8", errors = "ignore")
            if ch == "\x1b":
                ch += os.read(fd, 2).decode("utf-8", errors = "ignore")
                if ch == "\x1b[A":
                    return KEY_UP
                if ch == "\x1b[B":
                    return KEY_DOWN
                if ch == "\x1b[C":
                    return KEY_RIGHT
                if ch == "\x1b[D":
                    return KEY_LEFT
                else:
                    return KEY_ESC
            elif ch == "\r" or ch == "\n":
                return KEY_ENTER
            elif ch == "\x7f":
                return KEY_BACKSPACE
            elif ch.isprintable():
                return ch.lower()
            
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)