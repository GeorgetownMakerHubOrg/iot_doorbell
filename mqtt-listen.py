# GNU General Public License <https://www.gnu.org/licenses>
# Pascal Girard pascal.girard@georgetown.edu
import random, time, json, os
import paho.mqtt.client as mqtt

# Adafruit parameters
X_AIO_KEY = "aio_ouajbiadfad8fasdasdfasdfVOZ5"                       # Adafruit IO key
USER = "adafruit_user"                                               # Adafruit user
MQTT_SERVER = "io.adafruit.com"
MQTT_USER = USER
MQTT_PASSWD = X_AIO_KEY
MQTT_TOPIC = "gumakerhub/feeds/makerhubevents.backdoorbell"

username = MQTT_USER
password = MQTT_PASSWD

def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    # reconnect after losing the connection with the broker, it will continue to subscribe to the raspberry/topic topic
    client.subscribe(MQTT_TOPIC, qos=1)

# the callback function, it will be triggered when receiving messages
def on_message(client, userdata, msg):
    print('Payload is:', json.loads(msg.payload.decode()))
    print('Knock-knock')
    os.system("/home/pi/iot_doorbell/knock")

client = mqtt.Client()
client.username_pw_set(username, password)
client.on_connect = on_connect
client.on_message = on_message

# Connect with  broker address, broker port number, and keep-alive time respectively
client.connect(MQTT_SERVER, 1883, 60)

# Network loop blocking, it will not actively end the program before calling disconnect() or the program crash
client.loop_forever()
