#!/usr/bin/python3
import os
import schedule
from blink import blink
import time
import files
import firebase
import calculation

firebase.validateAccount()
#ledPin = 11
newBlink = blink()

def simpleJob():

    try:

        for i in range(10):
            newBlink.ledOn(0.5)
            newBlink.ledOff(0.5)

        #Get dateTime Now
        currentDatetime = files.currentTime()
        #Diccionario - firebase
        nodes = firebase.dicNodes(currentDatetime, calculation.genereRandomList(), calculation.genereRandomList(), calculation.genereRandomList(), calculation.genereRandomList(), calculation.genereRandomList())
        #firebase.validateAccount()
        firebase.insertData(nodes)
        #Add to logs.txt
        newMessage = 'New data added on:'
        nowConvert = files.dateTimeConvert(currentDatetime)
        files.manageFiles(message=newMessage ,time=nowConvert, status=True)

        for i in range(10):
            newBlink.ledOn(2)
            newBlink.ledOff(2)

    except:
        newBlink.ledOff()



def main():
    #schedule.every().hour.at(":27").do(simpleJob)
    schedule.every(2).minutes.do(simpleJob)
    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == "__main__":
    main()
