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
pd.options.display.float_format = '{:.2f}'.format


def main():
    file = "/home/pi/iot/rf24/weatherDatas.csv"
    firebase.validateAccount()
    df = pd.read_csv(file)

    #Capturar la hora actual - type -> datetime.datetime
    currentDatetime = files.currentTime()
    #Convertir la hora actual - type -> str
    currentDatetimeStr = files.dateTimeConvert(currentDatetime)

    for id, row in df.iterrows():
        if row.statusCloud == False:
            nodeOne=[row.airHumOne, row.airHumSensationOne, row.airTempOne, row.airTempSensationOne, row.earthHumOne, row.earthTempOne, row.lightOne]
            nodeTwo=[row.airHumTwo, row.airHumSensationTwo, row.airTempTwo, row.airTempSensationTwo, row.earthHumTwo, row.earthTempTwo, row.lightTwo]
            nodeThree=[row.airHumThree, row.airHumSensationThree, row.airTempThree, row.airTempSensationThree, row.earthHumThree, row.earthTempThree, row.lightThree]
            nodeFour=[row.airHumFour, row.airHumSensationFour, row.airTempFour, row.airTempSensationFour, row.earthHumFour, row.earthTempFour, row.lightFour]
            nodeFive=[row.airHumFive, row.airHumSensationFive, row.airTempFive, row.airTempSensationFive, row.earthHumFive, row.earthTempFive, row.lightFive]

            print(id)
            #Convertir de str de la fila csv a tipo datetime.datetime
            telemetryTime = files.strToTime(row.dateCaptured)

            #Diccionario - firebase
            #currentDatetime --> hora de envio a la nube
            #telemetryTime --> hora de datos capturados
            #nodes = firebase.dicNodes(currentDatetime, telemetryTime, nodeOne, nodeTwo, nodeThree, nodeFour, nodeFive)
            #firebase.insertData(nodes)

            telemetryTimeStr = files.dateTimeConvert(telemetryTime)
            df.at[id,'dateCaptured'] = telemetryTimeStr
            df.at[id,'statusCloud'] = True
            df.at[id,'timeSent'] = currentDatetimeStr

    #Add to logs.txt
    newMessage = 'New data added on:'
    nowConvert = files.dateTimeConvert(files.currentTime())
    files.manageFiles(message=newMessage ,time=nowConvert, status=True)

    df.to_csv(file, index=False, float_format='%.2f')

if __name__ == "__main__":
    main()
