# Micropython code for Georgetown Maker Hub's IOT Doorbell

# Since it's only a doorbell, the only other 'cool' feature is that it posts uptime() to io.adafruit.com
# Once you're sure that doorbell.py is properly functioning on the ESP8266, 
# use os.rename('doorbell.py','main.py') to have it load at boottime.

# The monitor uses the following components:
# - D1 Mini Wemos ESP8266 
# - Single Neopixel for Status
# - Simple push button

# See accompanying Fritzing diagram for circuitry.
# Still to do:
#    - Make upgrade module *really* work
#    - Make a box - thinking matchbox.

from machine import Pin, Signal, Timer, RTC
import os, utime, machine, esp, network, urequests, json
from neopixel import NeoPixel
import upgrade

pin0 = Pin(0, Pin.OUT)               # set GPIO0 to output to drive NeoPixels
pin2 = Pin(2, Pin.IN, Pin.PULL_UP)   # set GPIO12 as input with pullup
button = Signal(pin2, invert=True)   # let's use Signals, eh?
pressed = False
brightness = 128

# Change these to match your unique identifiers
# - wifi 
SSID = 'FooBar'
Password = 'SecretWord'
# - io.adafruit.com 
X_AIO_Key = '4f50c52123232312334ac7582c63ed'
User = 'Adafruit-Login'
Feed = 'Feed-Name'

np = NeoPixel(pin0, 1) 
np[0] = (0,0, brightness)
np.write()

def LED(r, g, b):
	np[0] = (r,g,b)
	np.write()

def do_connect():
	wlan = network.WLAN(network.STA_IF) 
	wlan.active(True)
	if not wlan.isconnected():
		print('Connecting to Network...')
		wlan.connect(SSID, Password)
		while not wlan.isconnected():
			pass
	print('Network Configuration (IP/GW/DNS1/DNS2): ', wlan.ifconfig())

def do_post(uptime):
	headers = {'X-AIO-Key': X_AIO_Key,'Content-Type': 'application/json'}
	url='https://io.adafruit.com/api/v2/'+User+'/feeds/'+Feed+'/data.json'
	data = json.dumps({"value": uptime/60000})
	# POST response
	response = urequests.post(url, headers=headers, data=data)
	# if not response.ok:
	#	print ("Error Posting to Adafruit") # what should we do?
	response.close()

ap = network.WLAN(network.AP_IF) # let's make sure we don't boot as an Access Point
ap.active(False)
while True:
	if not pressed and button.value():  # falling edge - button was pressed
		print("Button Pressed")
		LED(0,brightness,0)
		pressed = True
		uptime = utime.ticks_ms()
		# if connecting, posting and/or pressing button > 30s, let's launch WebREPL and debug...
		tim = Timer(-1)
		tim.init(period=30000, mode=Timer.ONE_SHOT, callback=lambda t:upgrade.start())
		do_connect()
		do_post(uptime)
	elif pressed and not button.value():   # rising edge - released button
		print("Button Released")
		LED(0,0,brightness)
		pressed = False
		tim.deinit()
	utime.sleep(0.01)
