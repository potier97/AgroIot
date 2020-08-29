#!/usr/bin/python3
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import json

class mqttThing():
    def __init__(self, thingName="GREENHOUSE-GATEWAY", awsHost="a2ejpqeqsr9chb-ats.iot.us-east-1.amazonaws.com", awsPort=8883, keyPath="/home/pi/iot/credentials/cabed16f65-private.pem.key", certPath="/home/pi/iot/credentials/cabed16f65-certificate.pem.crt", certCAPath="/home/pi/iot/credentials/AmazonRootCA1.pem"):
        self.thingName  = thingName    # ThingName
        self.awsHost    = awsHost      # EndPoint
        self.awsPort    = awsPort      # Port.No
        self.keyPath    = keyPath      # <Thing_Name>.pem.key
        self.certPath   = certPath     # <Thing_Name>.pem.crt
        self.certCAPath = certCAPath   # <Thing_Name>.pem
        self.mqttClient = AWSIoTMQTTClient(self.thingName)

    def configure(self):
        self.mqttClient.configureEndpoint(self.awsHost, self.awsPort)
        self.mqttClient.configureCredentials(self.certCAPath, self.keyPath, self.certPath)
        # Infinite offline Publish queueing
        self.mqttClient.configureOfflinePublishQueueing(-1)

    def connect(self):
        self.mqttClient.connect()

    def disconnect(self):
        self.mqttClient.disconnect()

    def publich(self, topic="iot/test", message='test message utf-8'):
        self.mqttClient.publish(topic, message, 0)

    def toJson(self, data):
        newJson= json.dumps(data, indent=4)
        return newJson



def main():
    import random
    data = {
        "nodeId0": {
            "temperature": round(random.uniform(0.00, 90.00), 2),
            "humidity": round(random.uniform(0.00, 90.00), 2),
            "light": round(random.uniform(0.00, 65000.00), 2)
        }
    }
    newThing=mqttThing()
    newThing.configure()
    newThing.connect()
    y = newThing.toJson(data)
    print(y)
    newThing.publich(topic="iot/nodes/sensors", message=y)
    newThing.disconnect()

if __name__ == "__main__":
    main()

