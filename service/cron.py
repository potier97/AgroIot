#!/usr/bin/python3
import os
import schedule
import time
from blink import blink



def SimpleJob():

    #ledPin = 11
    newBlink = blink()

    for i in range(30):
        newBlink.ledOn(1)
        newBlink.ledOff(1)
        print("30 Times of {}".format(i))



def main():
    try:
        schedule.every().day.at("00:00").do(simpleJob)

        while True:
            schedule.run_pending()
            time.sleep(1)
    except:
        newBlink.ledOff()
    finally:
        print ("Cron Script Stopped")



if __name__ == "__main__":
    main()

