# -*- coding = utf-8 -*-
# @Time : 2022/10/24 10:22
# @Author : cxk
# @File : z_ctypes.py
# @Software : PyCharm

"""
封装了专门为fps aimbot设计的键盘鼠标接口
对外接口：
moveRel(x_offset, y_offset)
    将鼠标移动一段向量(x_offset, y_offset)
leftClick(delay=0)
    鼠标左键连续按压 delay s
"""
import ctypes
import time

LONG = ctypes.c_long
DWORD = ctypes.c_ulong
ULONG_PTR = ctypes.POINTER(DWORD)
WORD = ctypes.c_ushort

INPUT_MOUSE = 0
MOUSEEVENTF_LEFTDOWN = 0x2
MOUSEEVENTF_LEFTUP = 0x4

KEYEVENTF_KEYUP=2
KEYEVENTF_KEYDOWN=0

class MouseInput(ctypes.Structure):
    _fields_ = [
        ('dx', LONG),
        ('dy', LONG),
        ('mouseData', DWORD),
        ('dwFlags', DWORD),
        ('time', DWORD),
        ('dwExtraInfo', ULONG_PTR)
    ]


class InputUnion(ctypes.Union):
    _fields_ = [
        ('mi', MouseInput)
    ]


class Input(ctypes.Structure):
    _fields_ = [
        ('types', DWORD),
        ('iu', InputUnion)
    ]


def mouse_input_set(flags, x, y, data):
    return MouseInput(x, y, data, flags, 0, None)


def input_do(structure):
    if isinstance(structure, MouseInput):
        return Input(INPUT_MOUSE, InputUnion(mi=structure))
    raise TypeError('Cannot create Input structure!')


def mouse_input(flags, x=0, y=0, data=0):
    return input_do(mouse_input_set(flags, x, y, data))


def SendInput(*inputs):
    n_inputs = len(inputs)
    lp_input = Input * n_inputs
    p_inputs = lp_input(*inputs)
    cb_size = ctypes.c_int(ctypes.sizeof(Input))
    return ctypes.windll.user32.SendInput(n_inputs, p_inputs, cb_size)

def moveRel(x_offset, y_offset):
    SendInput(mouse_input(1, x_offset, y_offset))




CLICK_INTERVAL = 0.005

def _leftClick(delay=0):
    "模拟鼠标左键单击"
    try:
        ctypes.windll.user32.mouse_event(MOUSEEVENTF_LEFTDOWN)
    except ValueError as err: # 同上
        ctypes.windll.warn("ValueError: "+str(err))
    time.sleep(delay/2)
    try:
        ctypes.windll.user32.mouse_event(MOUSEEVENTF_LEFTUP)
    except ValueError as err:
        ctypes.windll.warn("ValueError: "+str(err))
    time.sleep(delay/2)

def leftClick(delay: float=0) -> None:
    """鼠标左键连续按压 delay s"""
    for i in range(int(delay / CLICK_INTERVAL)):
        _leftClick(CLICK_INTERVAL)



def _keyPress(key, delay=0.05):
    "模拟键盘中字母key(大写)单击"
    try:
        ctypes.windll.user32.keybd_event(ord(key), 0, KEYEVENTF_KEYDOWN, 0)
    except ValueError as err: # 同上
        ctypes.windll.warn("ValueError: "+str(err))
    time.sleep(delay/2)

    try:
        ctypes.windll.user32.keybd_event(ord(key), 0, KEYEVENTF_KEYUP, 0)
    except ValueError as err: # 同上
        ctypes.windll.warn("ValueError: "+str(err))
    time.sleep(delay/2)


def keyPress(key: chr, delay: float =0)-> None:
    """键盘中的key(要求大写)被连续按压 delay s"""
    id = ord(key)
    if id >= ord('A') and id <= ord('Z'): 
        for i in range(int(delay / 0.003)):
            _keyPress(key, 0.003)
        return
    raise("key must be lowercase alphabet")

if __name__ == '__main__':
    # SendInput(mouse_input(1, -100, -200))
    time.sleep(2)
    leftClick(1)