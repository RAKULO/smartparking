import paho.mqtt.client as mqtt
import random

topic_root = "SERVER/on"
def on_connect(client, userdata, flags, rc):
  print("Connected with result code "+ str(rc))
  client.subscribe(topic_root)

def on_message(client, userdata, msg):
  t0 = random.randint(0,30)
  print(msg.topic+msg.payload.decode('utf-8'))
  client.publish("PLATE/", t0)

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
# client.username_pw_set("test", "1234")
client.connect("220.132.124.155", 1883, 60)
client.loop_forever()