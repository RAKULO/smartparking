import paho.mqtt.client as mqtt
import random
import json
import datetime
import time

ISOTIMEFORMAT = '%m/%d %H:%M:%S'
client = mqtt.Client()
# client.username_pw_set("test", "1234")
print("set ok")
# client.connect("220.132.124.155", 1883, 60)
client.connect("127.0.0.1", 1883, 60)

while True:
  # t = datetime.datetime.now().strftime(ISOTIMEFORMAT)
  # payload = {'Temperature' : t0, 'Time' : t}
  # print(json.dumps(payload)) 
  # client.publish("SERVER/on", json.dumps(payload))
  t0 = random.randint(0,1)
  print(t0)
  client.publish("SERVER/on", t0)
  time.sleep(5)