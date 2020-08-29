#!/usr/bin/python3
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from dataStructure import struct


def validateAccount():
    serviceAccount="telemetryiot-firebase-adminsdk-ip9yj-d5e016348c.json"
    cred = credentials.Certificate(serviceAccount)
    firebase_admin.initialize_app(cred)

def insertData(data):
    collectionName="NODES-WEATHER"
    db = firestore.client()
    newDoc = db.collection(collectionName).document()
    newDoc.set(data)



def main():
    import random
    import json
    #se crea un diccionario
    z = struct("19/08/2020 23:11:01", round(random.uniform(0.00, 90.00), 2), round(random.uniform(0.00, 90.00), 2),
        round(random.uniform(0.00, 90.00), 2), round(random.uniform(0.00, 90.00), 2), round(random.uniform(0.00, 90.00), 2), round(random.uniform(0.00, 90.00), 2), round(random.uniform(0.00, 90.00), 2),
        round(random.uniform(0.00, 90.00), 2), round(random.uniform(0.00, 90.00), 2), round(random.uniform(0.00, 90.00), 2), round(random.uniform(0.00, 90.00), 2), round(random.uniform(0.00, 90.00), 2),
        round(random.uniform(0.00, 90.00), 2), round(random.uniform(0.00, 90.00), 2), round(random.uniform(0.00, 90.00), 2), round(random.uniform(0.00, 90.00), 2), round(random.uniform(0.00, 90.00), 2),
        round(random.uniform(0.00, 90.00), 2), round(random.uniform(0.00, 90.00), 2), round(random.uniform(0.00, 90.00), 2), round(random.uniform(0.00, 90.00), 2), round(random.uniform(0.00, 90.00), 2),
        round(random.uniform(0.00, 90.00), 2), round(random.uniform(0.00, 90.00), 2), round(random.uniform(0.00, 90.00), 2), round(random.uniform(0.00, 90.00), 2), round(random.uniform(0.00, 90.00), 2),
        round(random.uniform(0.00, 90.00), 2), round(random.uniform(0.00, 90.00), 2), round(random.uniform(0.00, 90.00), 2), round(random.uniform(0.00, 90.00), 2), round(random.uniform(0.00, 90.00), 2),
        round(random.uniform(0.00, 90.00), 2), round(random.uniform(0.00, 90.00), 2), round(random.uniform(0.00, 90.00), 2), round(random.uniform(0.00, 90.00), 2), round(random.uniform(0.00, 90.00), 2),
        round(random.uniform(0.00, 90.00), 2), round(random.uniform(0.00, 90.00), 2), round(random.uniform(0.00, 90.00), 2), round(random.uniform(0.00, 90.00), 2), round(random.uniform(0.00, 90.00), 2))
    y = json.dumps(z, indent=4)
    print(y)
    validateAccount()
    insertData(z)




if __name__ == "__main__":
    main()

