#!/usr/bin/python3
import os
import schedule
from blink import blink
import time
import files
import firebase
import heatMap
import calculation
import time
import pandas as pd
pd.options.display.float_format = '{:.2f}'.format

firebase.validateAccount()
newBlink = blink()

def simpleJob():

    try:

        #Start to count time
        print("Iniciando a contar el tiempo")
        start = time.time()

        for i in range(10):
            newBlink.ledOn(0.25)
            newBlink.ledOff(0.25)

        #App Validate
        #firebase.validateAccount()

        fileName="/home/pi/iot/store/weatherDatas.csv"
        df = pd.read_csv(fileName)

        #Get dateTime Now
        currentDatetime = files.currentTime()
        #Convert date type to str
        currentDatetimeStr = files.dateTimeConvert(currentDatetime)


        for id, row in df.iterrows():
            if row.statusCloud == False:


                #View row id
                print(id)


                #Get data by node
                nodeOne   = [row.airHumOne, row.airHumSensationOne, row.airTempOne, row.airTempSensationOne, row.earthHumOne, row.earthTempOne, row.lightOne]
                nodeTwo   = [row.airHumTwo, row.airHumSensationTwo, row.airTempTwo, row.airTempSensationTwo, row.earthHumTwo, row.earthTempTwo, row.lightTwo]
                nodeThree = [row.airHumThree, row.airHumSensationThree, row.airTempThree, row.airTempSensationThree, row.earthHumThree, row.earthTempThree, row.lightThree]
                nodeFour  = [row.airHumFour, row.airHumSensationFour, row.airTempFour, row.airTempSensationFour, row.earthHumFour, row.earthTempFour, row.lightFour]
                nodeFive  = [row.airHumFive, row.airHumSensationFive, row.airTempFive, row.airTempSensationFive, row.earthHumFive, row.earthTempFive, row.lightFive]


                #Get captured data and convert str datetime to datetime.datetime
                telemetryTime = files.strToTime(row.dateCaptured)


                #get data by var
                #airHum0, airHumSensation0, airTemp0, airTempSensation0, earthHum0, earthTemp0, light0,
                airTemp   = [nodeOne[2], nodeTwo[2], nodeThree[2], nodeFour[2], nodeFive[2]]
                airHum    = [nodeOne[0], nodeTwo[0], nodeThree[0], nodeFour[0], nodeFive[0]]
                earthTemp = [nodeOne[5], nodeTwo[5], nodeThree[5], nodeFour[5], nodeFive[5]]
                earthHum  = [nodeOne[4], nodeTwo[4], nodeThree[4], nodeFour[4], nodeFive[4]]
                light     = [nodeOne[6], nodeTwo[6], nodeThree[6], nodeFour[6], nodeFive[6]]


                #Charts
                fileImagePath_AirTemp,   fileName_AirTemp   = heatMap.myPlot(0, airTemp,   currentDatetimeStr)
                fileImagePath_AirHum,    fileName_AirHum    = heatMap.myPlot(1, airHum,    currentDatetimeStr)
                fileImagePath_EarthTemp, fileName_EarthTemp = heatMap.myPlot(2, earthTemp, currentDatetimeStr)
                fileImagePath_EarthHum,  fileName_EarthHum  = heatMap.myPlot(3, earthHum,  currentDatetimeStr)
                fileImagePath_Light,     fileName_Light     = heatMap.myPlot(4, light,     currentDatetimeStr)


                #Upload image to Storage
                pathUrl_AirTemp   = firebase.insertFile(0, fileImagePath_AirTemp,   fileName_AirTemp)
                pathUrl_AirHum    = firebase.insertFile(1, fileImagePath_AirHum,    fileName_AirHum)
                pathUrl_EarthTemp = firebase.insertFile(2, fileImagePath_EarthTemp, fileName_EarthTemp)
                pathUrl_EarthHum  = firebase.insertFile(3, fileImagePath_EarthHum,  fileName_EarthHum)
                pathUrl_Light     = firebase.insertFile(4, fileImagePath_Light,     fileName_Light)


                #Create a Dic to send to firebase
                #currentDatetime --> Datetime to cloud sended
                #telemetryTime --> Captured data dateTime by wsn
                nodes = firebase.dicNodes(currentDatetime, telemetryTime,
                                 fileImagePath_AirTemp, fileImagePath_AirHum, fileImagePath_EarthTemp, fileImagePath_EarthHum, fileImagePath_Light,
                                 pathUrl_AirTemp, pathUrl_AirHum, pathUrl_EarthTemp, pathUrl_EarthHum, pathUrl_Light,
                                 nodeOne, nodeTwo, nodeThree, nodeFour, nodeFive)
                #print(nodes)

                #Send dato to Firestore
                #firebase.insertData(nodes)

                #Update data on csv
                df.at[id,'dateCaptured'] = files.dateTimeConvert(telemetryTime)
                df.at[id,'statusCloud'] = True
                df.at[id,'timeSent'] = currentDatetimeStr

        #Add logs.txt
        files.manageFiles(message='New data added on:', time=currentDatetimeStr)

        #Rewrite file with process
        df.to_csv(fileName, index=False, float_format='%.2f')


        for i in range(10):
            newBlink.ledOn(0.25)
            newBlink.ledOff(0.25)


        #Stop to cout time
        end = time.time()
        #Results
        print("Tiempo total para ejecutar el script: {:.3f} Segundos".format(end - start))


    except:
        newBlink.ledOff()



def main():
    #schedule.every().hour.at(":01").do(simpleJob)
    #while True:
    #    schedule.run_pending()
    #    time.sleep(1)
    simpleJob()


if __name__ == "__main__":
    main()
