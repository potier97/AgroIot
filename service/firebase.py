#!/usr/bin/python3
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import dataStructure
import files
import datetime
import calculation


def validateAccount():
    serviceAccount="/home/pi/iot/service/telemetryiot-firebase-adminsdk-ip9yj-d5e016348c.json"
    cred = credentials.Certificate(serviceAccount)
    firebase_admin.initialize_app(cred)

def insertData(data):
    collectionName="NODES-WEATHER"
    db = firestore.client()
    newDoc = db.collection(collectionName)
    newDoc.document().set(data)
    #return status

def dicNodes(stateTime, telemetryTime, nodeOne, nodeTwo, nodeThree, nodeFour, nodeFive, aditional=None):

    nodes = {}
    nodes['node01'] = nodeOne
    nodes['node02'] = nodeTwo
    nodes['node03'] = nodeThree
    nodes['node04'] = nodeFour
    nodes['node05'] = nodeFive
    nodes['node00'] = calculation.averageVar(nodes)

    dataNodeStructure = dataStructure.struct(stateTime , telemetryTime,
            nodes['node00'][0], nodes['node00'][1], nodes['node00'][2], nodes['node00'][3], nodes['node00'][4], nodes['node00'][5], nodes['node00'][6],
            nodes['node01'][0], nodes['node01'][1], nodes['node01'][2], nodes['node01'][3], nodes['node01'][4], nodes['node01'][5], nodes['node01'][6],
            nodes['node02'][0], nodes['node02'][1], nodes['node02'][2], nodes['node02'][3], nodes['node02'][4], nodes['node02'][5], nodes['node02'][6],
            nodes['node03'][0], nodes['node03'][1], nodes['node03'][2], nodes['node03'][3], nodes['node03'][4], nodes['node03'][5], nodes['node03'][6],
            nodes['node04'][0], nodes['node04'][1], nodes['node04'][2], nodes['node04'][3], nodes['node04'][4], nodes['node04'][5], nodes['node04'][6],
            nodes['node05'][0], nodes['node05'][1], nodes['node05'][2], nodes['node05'][3], nodes['node05'][4], nodes['node05'][5], nodes['node05'][6])

    return dataNodeStructure


def main():
    currentDatetime = files.currentTime()

    #Diccionario - firebase
    nodes = dicNodes(currentDatetime, currentDatetime, calculation.genereRandomList(), calculation.genereRandomList(), calculation.genereRandomList(), calculation.genereRandomList(), calculation.genereRandomList())
    print(nodes)
    validateAccount()
    insertData(nodes)
    #Add to logs.txt
    newMessage = 'New data added on:'
    nowConvert = files.dateTimeConvert(currentDatetime)
    files.manageFiles(message=newMessage ,time=nowConvert, status=True)



if __name__ == "__main__":
    main()

