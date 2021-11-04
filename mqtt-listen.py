import random, time, json, requests, os
import config 

from paho.mqtt import client as mqtt_client

broker = config.MQTT_SERVER
port = 1883
topic = config.MQTT_SUB_TOPIC
# generate client ID with random suffix
client_id = "doorbell-mqtt-test-"+str(random.getrandbits(16))
username = config.MQTT_USER
password = config.MQTT_PASSWD

# Reasonable default values

data = {"count": 0}

def connect_mqtt() -> mqtt_client:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)
    client = mqtt_client.Client(client_id)
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client

def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        global data
        print('Payload is:', json.loads(msg.payload.decode()))
        data['count'] += 1
        os.system("/home/pi/iot_doorbell/knock")
    client.subscribe(topic)
    client.on_message = on_message
print("client id is: ", client_id)
client = connect_mqtt()
subscribe(client)
client.loop_forever()
