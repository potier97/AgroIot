#!/usr/bin/python3
import RPi.GPIO as GPIO
import time


#7 indica el numero en de la posición en la placa de la Rpi
#GPIO 4 - PIN 7
#DNS    - PIN 9



class blink():

    def __init__(self, ledPin=11):
        self.ledPin=ledPin
        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)
        GPIO.setup(ledPin, GPIO.OUT)

    def ledOn(self, delay=0.5):
        GPIO.output(self.ledPin, True)
        time.sleep(delay)

    def ledOff(self, delay=0.5):
        GPIO.output(self.ledPin, False)
        time.sleep(delay)

    def cicle(self, status=True):
        while status:
            self.ledOn()
            self.ledOff() 



def main():
    try:
        #ledPin = 11
        newBlink = blink()
        while True:
            newBlink.ledOn()
            newBlink.ledOff()
    except:
        newBlink.ledOff()
    finally:
        print ("Script Stopped")




if __name__ == "__main__":
    main()
