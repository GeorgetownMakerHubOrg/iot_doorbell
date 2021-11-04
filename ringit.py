import time, requests, json
import config

Feed = 'makerhubevents.backdoorbell'

def do_post():
   headers = {'X-AIO-Key': config.X_AIO_KEY,'Content-Type': 'application/json'}
   url='https://io.adafruit.com/api/v2/'+config.USER+'/feeds/'+Feed+'/data.json'
   data = json.dumps({"value": 10})
   # POST response
   response = requests.post(url, headers=headers, data=data)
   # if not response.ok:
   print("Adafruit's response is: ", response.text)
   #print ("Error Posting to Adafruit") # what should we do?
   response.close()

while True:
   print('Posting on Adafruit')
   do_post()
   time.sleep(30)
