### sys_fun ###
import os
import sys


def clear():
    if sys.platform[:3] == "win":
        os.system("cls")
    if sys.platform[:5] == "linux" or sys.platform[:6] == "darwin":
        os.system("clear")
