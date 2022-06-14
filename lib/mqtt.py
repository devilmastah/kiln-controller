import paho.mqtt.client as mqtt #import the client1
import json
import config

class sendMqttdata():
    def __init__(self):
        if config.useMQTT:
            self.client = mqtt.Client("P1") #create new instance
            self.client.username_pw_set(config.username, config.password)
            self.client.connect(config.MQTTBroker) #connect to broker
       
        self.publishablestate = {
            'devicename':config.devicename,
            'heaterpower': 0,
            'targettemperature':0,
            'timeleftminutes':0,
            'timeleftseconds':0,
            'kilnstate':"UNKNOWN",
            'alert':"UNKNOWN",
            "activeprofile":"UNKNOWN",
            "keepalive": 0
        }

    def updatePublishData(self, sendkey, value):
        self.publishablestate[sendkey] = value
      
        
    def publishData(self):
        if config.useMQTT:
            self.client.publish("shed/"+config.devicename,json.dumps(self.publishablestate))