#!/usr/bin/python3
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from firebase_admin import storage
import requests
import dataStructure
import files
import datetime
import calculation
import heatMap

def validateAccount():
    serviceAccount="/home/pi/iot/credentials/telemetryiot-firebase-adminsdk-ip9yj-3413172e15.json"
    cred = credentials.Certificate(serviceAccount)
    firebase_admin.initialize_app(cred)

def insertData(data):
    collectionName="NODES-WEATHER"
    db = firestore.client()

    newDoc = db.collection(collectionName)
    newDoc.document().set(data)
    #return status

def deleteData():
    #import time
    collectionName="NODES-WEATHER"
    db = firestore.client()
    docs = db.collection(collectionName).stream()
    for doc in  docs:
        print(doc.id)
        db.collection(collectionName).document(doc.id).delete()
    return "newDoc"


def insertFile(varPath, filePath, cloudPath):

    labelName = ''
    if varPath == 0:
        labelName = 'temperaturaAire/' + cloudPath
    elif varPath == 1:
        labelName = 'humedadAire/' + cloudPath
    elif varPath == 2:
        labelName = 'temperaturaTierra/' + cloudPath
    elif varPath == 3:
        labelName = 'humedadTierra/' + cloudPath
    elif varPath == 4:
        labelName = 'luz/' + cloudPath

    Bucket = storage.bucket("telemetryiot.appspot.com")
    #blob = Bucket.blob(cloudPath)
    #blob.delete()
    newBlob = Bucket.blob(labelName)
    newBlob.upload_from_filename(filePath)
    newBlob.make_public()
    return newBlob.public_url


def dicNodes(stateTime, telemetryTime, pathAt, pathAh, pathEt, pathEh, pathL, urlAt, urlAh, urlEt, urlEh, urlL, nodeOne, nodeTwo, nodeThree, nodeFour, nodeFive):

    nodes = {}
    nodes['node01'] = nodeOne
    nodes['node02'] = nodeTwo
    nodes['node03'] = nodeThree
    nodes['node04'] = nodeFour
    nodes['node05'] = nodeFive
    nodes['node00'] = calculation.averageVar(nodes)

    dataNodeStructure = dataStructure.struct(stateTime, telemetryTime, pathAt, pathAh, pathEt, pathEh, pathL, urlAt, urlAh, urlEt, urlEh, urlL,
            nodes['node00'][0], nodes['node00'][1], nodes['node00'][2], nodes['node00'][3], nodes['node00'][4], nodes['node00'][5], nodes['node00'][6],
            nodes['node01'][0], nodes['node01'][1], nodes['node01'][2], nodes['node01'][3], nodes['node01'][4], nodes['node01'][5], nodes['node01'][6],
            nodes['node02'][0], nodes['node02'][1], nodes['node02'][2], nodes['node02'][3], nodes['node02'][4], nodes['node02'][5], nodes['node02'][6],
            nodes['node03'][0], nodes['node03'][1], nodes['node03'][2], nodes['node03'][3], nodes['node03'][4], nodes['node03'][5], nodes['node03'][6],
            nodes['node04'][0], nodes['node04'][1], nodes['node04'][2], nodes['node04'][3], nodes['node04'][4], nodes['node04'][5], nodes['node04'][6],
            nodes['node05'][0], nodes['node05'][1], nodes['node05'][2], nodes['node05'][3], nodes['node05'][4], nodes['node05'][5], nodes['node05'][6])

    return dataNodeStructure


def main():
    #Count time
    import time


    #Start to count time
    print("Iniciando a contar el tiempo")
    start = time.time()
    """
    #Validate App
    validateAccount()


    #Get dateTime now
    currentDatetime = files.currentTime()
    #Convert dateTime to str
    currentDatetimeStr = files.dateTimeConvert(currentDatetime)

    #Random Data
    airTemp =  calculation.genereRandomList()
    airHum = calculation.genereRandomList()
    earthTemp = calculation.genereRandomList()
    earthHum =  calculation.genereRandomList()
    light = calculation.genereRandomList()

    #Charts
    fileImagePath_AirTemp,   fileName_AirTemp   = heatMap.myPlot(0, airTemp, currentDatetimeStr)
    fileImagePath_AirHum,    fileName_AirHum    = heatMap.myPlot(1, airHum, currentDatetimeStr)
    fileImagePath_EarthTemp, fileName_EarthTemp = heatMap.myPlot(2, earthTemp, currentDatetimeStr)
    fileImagePath_EarthHum,  fileName_EarthHum  = heatMap.myPlot(3, earthHum, currentDatetimeStr)
    fileImagePath_Light,     fileName_Light     = heatMap.myPlot(4, light, currentDatetimeStr)

    #Upload image to Storage
    pathUrl_AirTemp   = insertFile(0, fileImagePath_AirTemp,   fileName_AirTemp)
    pathUrl_AirHum    = insertFile(1, fileImagePath_AirHum,    fileName_AirHum)
    pathUrl_EarthTemp = insertFile(2, fileImagePath_EarthTemp, fileName_EarthTemp)
    pathUrl_EarthHum  = insertFile(3, fileImagePath_EarthHum,  fileName_EarthHum)
    pathUrl_Light     = insertFile(4, fileImagePath_Light,     fileName_Light)


    #Set Dic - firebase
    nodes = dicNodes(currentDatetime, currentDatetime,
                     fileImagePath_AirTemp, fileImagePath_AirHum, fileImagePath_EarthTemp, fileImagePath_EarthHum, fileImagePath_Light,
                     pathUrl_AirTemp, pathUrl_AirHum, pathUrl_EarthTemp, pathUrl_EarthHum, pathUrl_Light,
                     airTemp, airHum, earthTemp, earthHum, light)
    #print(nodes)

    #Put data to firestore
    insertData(nodes)

    #Add to logs.txt
    newMessage = 'New data added on:'
    nowConvert = files.dateTimeConvert(currentDatetime)
    files.manageFiles(message=newMessage ,time=nowConvert, status=True)
    """
    validateAccount()
    deleteData()


    #Stop to cout time
    end = time.time()
    #Results
    print("Tiempo total para ejecutar el script: {:.3f} Segundos".format(end - start))


if __name__ == "__main__":
    main()

