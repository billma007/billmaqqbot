#!/usr/bin/python
# -*- coding: utf-8 -*-
import platform
debugit=False
SYSTEM=platform.system()

import time
class CommonColor():
    GRAY=30
    RED=31
    GREEN=32
    YELLOW=33
    BLUE=34
    MAGENTA=35
    CYAN=36
    WHITE=37
    CRIMSON=38 

def colorize(num):
    if num==0x0a:
        print("\033[92m",end='')
    elif num==0x0b:
        print("\033[94m",end='')
    elif num==0x0f:
        print("\033[0m",end='')
    elif num==0x0b:
        print("\033[93m",end='')
    elif num==0x0c:
        print("\033[91m",end='')
'''
在windows系统下可以通过修改底层来修改颜色
'''


class WindowsColor():
    FOREGROUND_BLACK = 0x00 # black.
    FOREGROUND_DARKBLUE = 0x01 # dark blue.
    FOREGROUND_DARKGREEN = 0x02 # dark green.
    FOREGROUND_DARKSKYBLUE = 0x03 # dark skyblue.
    FOREGROUND_DARKRED = 0x04 # dark red.
    FOREGROUND_DARKPINK = 0x05 # dark pink.
    FOREGROUND_DARKYELLOW = 0x06 # dark yellow.
    FOREGROUND_DARKWHITE = 0x07 # dark white.
    FOREGROUND_DARKGRAY = 0x08 # dark gray.
    FOREGROUND_BLUE = 0x09 # blue.
    FOREGROUND_GREEN = 0x0a # green.
    FOREGROUND_SKYBLUE = 0x0b # skyblue.
    FOREGROUND_RED = 0x0c # red.
    FOREGROUND_PINK = 0x0d # pink.
    FOREGROUND_YELLOW = 0x0e # yellow.
    FOREGROUND_WHITE = 0x0f # white.
    BACKGROUND_BLUE = 0x10 # dark blue.
    BACKGROUND_GREEN = 0x20 # dark green.
    BACKGROUND_DARKSKYBLUE = 0x30 # dark skyblue.
    BACKGROUND_DARKRED = 0x40 # dark red.
    BACKGROUND_DARKPINK = 0x50 # dark pink.
    BACKGROUND_DARKYELLOW = 0x60 # dark yellow.
    BACKGROUND_DARKWHITE = 0x70 # dark white.
    BACKGROUND_DARKGRAY = 0x80 # dark gray.
    BACKGROUND_BLUE = 0x90 # blue.
    BACKGROUND_GREEN = 0xa0 # green.
    BACKGROUND_SKYBLUE = 0xb0 # skyblue.
    BACKGROUND_RED = 0xc0 # red.
    BACKGROUND_PINK = 0xd0 # pink.
    BACKGROUND_YELLOW = 0xe0 # yellow.
    BACKGROUND_WHITE = 0xf0 # white.

if SYSTEM=="Windows" or SYSTEM=="windows":
    import ctypes
    from subprocess import STD_OUTPUT_HANDLE
    std_out_handle = ctypes.windll.kernel32.GetStdHandle(STD_OUTPUT_HANDLE)
    
def set_cmd_text_color(color):
    if SYSTEM=="Windows" or SYSTEM=="windows":
        handle=std_out_handle
        import ctypes
        Bool = ctypes.windll.kernel32.SetConsoleTextAttribute(handle, color)
        return Bool
    else:
        colorize(color)
def timenow():
                local_times = time.localtime(time.time())
                local_time_asctimes = time.asctime(local_times)
                return str(local_time_asctimes)
def info(msg):# info
                set_cmd_text_color(0x0b)
                print("["+timenow()+"]",end='')
                set_cmd_text_color(0x0f)
                print("[INFO]"+str(msg))
def success(msg):
                set_cmd_text_color(0x0b)
                print("["+timenow()+"]",end='')
                set_cmd_text_color(0x0a)
                print("[SUCCESS]"+str(msg))
                set_cmd_text_color(0x0f)
def error(msg):
                set_cmd_text_color(0x0b)
                print("["+timenow()+"]",end='')
                set_cmd_text_color(0x0c)
                print("[ERROR]"+str(msg))
                set_cmd_text_color(0x0f)
def warning(msg):
                set_cmd_text_color(0x0b)
                print("["+timenow()+"]",end='')
                set_cmd_text_color(0x0e)
                print("[WARNING]"+str(msg))
                set_cmd_text_color(0x0f)
def debug(msg):
                if debugit==True:
                    print(msg)