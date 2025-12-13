from EasyPy import wait
from .Discord import *
from .Math import *
"""EasyPy, Easy Python, Simples"""
def Run(target):
    target()
def Loop(target,looping:bool):
    while looping:
        target()

