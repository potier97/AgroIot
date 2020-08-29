#!/usr/bin/python3

import os
import schedule
import time
from blink import blink




def main():
    try:
        #ledPin = 11
        newBlink = blink()

        def simpleJob():
            simpleList = [1,2,3,4,5,6,7,8,9,10]
            for i in simpleList:
                newBlink.ledOn(1)
                newBlink.ledOff(1)
                print("{} Times of {}".format(len(simpleList), i))

        #schedule.every().minutes.do(simpleJob)
        schedule.every().day.at("00:00").do(simpleJob)
        schedule.every().day.at("01:00").do(simpleJob)
        schedule.every().day.at("02:00").do(simpleJob)
        schedule.every().day.at("03:00").do(simpleJob)
        schedule.every().day.at("04:00").do(simpleJob)
        schedule.every().day.at("05:00").do(simpleJob)
	schedule.every().day.at("06:00").do(simpleJob)
        schedule.every().day.at("07:00").do(simpleJob)
        schedule.every().day.at("08:00").do(simpleJob)
        schedule.every().day.at("09:00").do(simpleJob)
        schedule.every().day.at("10:00").do(simpleJob)
        schedule.every().day.at("11:00").do(simpleJob)
        schedule.every().day.at("12:00").do(simpleJob)
        schedule.every().day.at("13:00").do(simpleJob)
        schedule.every().day.at("13:00").do(simpleJob)
        schedule.every().day.at("14:00").do(simpleJob)
        schedule.every().day.at("15:00").do(simpleJob)
        schedule.every().day.at("16:00").do(simpleJob)
        schedule.every().day.at("17:00").do(simpleJob)
        schedule.every().day.at("18:00").do(simpleJob)
        schedule.every().day.at("19:00").do(simpleJob)
        schedule.every().day.at("20:00").do(simpleJob)
        schedule.every().day.at("21:00").do(simpleJob)
        schedule.every().day.at("22:00").do(simpleJob)
        schedule.every().day.at("23:00").do(simpleJob)

        while True:
            schedule.run_pending()
            time.sleep(1)
    except:
        newBlink.ledOff()
    finally:
        print ("Cron Script Stopped")



if __name__ == "__main__":
    main()

