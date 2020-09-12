#!/usr/bin/python3
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import dataStructure
import firebase
import files
import datetime
import calculation
import os
import time
import files
import pandas as pd



def main():
    file = "/home/pi/iot/rf24/weatherData.csv"
    firebase.validateAccount()
    df = pd.read_csv(file)

    for id, row in df.iterrows():
        if row.statusCloud == False:
            nodeOne=[row.airHumOne, row.airHumSensationOne, row.airTempOne, row.airTempSensationOne, row.earthHumOne, row.earthTempOne, row.lightOne]
            nodeTwo=[row.airHumTwo, row.airHumSensationTwo, row.airTempTwo, row.airTempSensationTwo, row.earthHumTwo, row.earthTempTwo, row.lightTwo]
            nodeThree=[row.airHumThree, row.airHumSensationThree, row.airTempThree, row.airTempSensationThree, row.earthHumThree, row.earthTempThree, row.lightThree]
            nodeFour=[row.airHumFour, row.airHumSensationFour, row.airTempFour, row.airTempSensationFour, row.earthHumFour, row.earthTempFour, row.lightFour]
            nodeFive=[row.airHumFive, row.airHumSensationFive, row.airTempFive, row.airTempSensationFive, row.earthHumFive, row.earthTempFive, row.lightFive]

            print(id)
            telemetryTime = files.strToTime(row.dateCaptured)
            currentDatetime = files.currentTime()
            #Diccionario - firebase
            nodes = firebase.dicNodes(currentDatetime, telemetryTime, nodeOne, nodeTwo, nodeThree, nodeFour, nodeFive)
            firebase.insertData(nodes)
            #Add to logs.txt
            newMessage = 'New data added on:'
            nowConvert = files.dateTimeConvert(currentDatetime)
            files.manageFiles(message=newMessage ,time=nowConvert, status=True)

            df.at[id,'statusCloud']= True
            df.at[id,'timeSent']= row.dateCaptured

    df.to_csv(file, index=False)





if __name__ == "__main__":
    main()
