from numpy import angle
import time
from pyfirmata import Arduino, SERVO
port='COM3'

pin=10

board=Arduino(port)
board.digital[pin].mode=SERVO

def rotateservo(pin,angle):
    board.digital[pin].write(angle)

def doorautomate(value):
    if value == 0:#open
        rotateservo(pin, 180)
    elif value == 1: #lock
        rotateservo(pin, 40)


