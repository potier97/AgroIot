#!/usr/bin/python3
from blink import blink
import time



newBlink = blink()
#print('hello world')

try:
    #ledPin = 11
    #newBlink = blink()
    while True:
        newBlink.ledOn(0.1)
        newBlink.ledOff(0.1)
except:
    newBlink.ledOff()




