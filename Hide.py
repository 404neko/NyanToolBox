#-*- coding:utf-8 -*-

import ctypes

WindowsHide=ctypes.windll.kernel32.GetConsoleWindow()
if WindowsHide!=0:
    ctypes.windll.user32.ShowWindow(WindowsHide,0)
    ctypes.windll.kernel32.CloseHandle(WindowsHide)

#If you want to hide pythons' windows on WindowsOS please'from Hide import *'