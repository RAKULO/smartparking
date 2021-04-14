#!/usr/bin/python
import time
import os
import datetime
import subprocess
import json
import sys
import random
import base64
import paho.mqtt.client as mqtt

#建立MQTT_SUB
topic_command_root = "SERVER/on"
plate_root = "PLATE/"
plate_img_root = "PLATE/img"
host = "220.132.124.155"
host_local = "127.0.0.1"

def on_connect(client, userdata, flags, rc):
  print("Connected with result code "+ str(rc))
  client.subscribe(topic_command_root)

def on_message(client, userdata, msg):
  MSG = msg.payload.decode('utf-8')
  if MSG == "0":
    # t = "DO NOT DO ANYTHING"
    client.publish("PLATE/", qos=1)
    print("FROM: "+msg.topic+" OP: "+msg.payload.decode('utf-8')+" DO: "+"DO NOT DO ANYTHING")

  elif MSG == "1":
    # 忽略前20幀，捕捉第21幀影像並存至指定位置
    webcam_command = "fswebcam  -r 640x480 -S 20 --save /root/RTSP/alpr.jpg -q"
    subprocess.Popen(webcam_command, shell=True)
    # 讀取捕獲之圖片檔，投入辨識並回傳JSON
    alpr_command = "alpr -c us /Users/PingHsiLo/Desktop/3317LS.jpeg -j" 
    lp_data = json.loads(subprocess.check_output(alpr_command, shell=True).decode(sys.stdout.encoding))
  
    try:
      IMAGE_PATH = "/Users/PingHsiLo/Desktop/3317LS.jpeg"
      #試將JSON中result的車牌值設給lp_number
      lp_number = lp_data["results"][0]['plate']
      #將JSON中result的epohtime值設給ID
      # lp_id = lp_data["epoch_time"]
      client.publish(plate_root, lp_number, qos=1)
      print("FROM: "+msg.topic+" OP: "+msg.payload.decode('utf-8')+" DO: "+lp_number)
      with open(IMAGE_PATH, 'rb') as image_file:
        img_base64 = base64.b64encode(image_file.read())
        client.publish(plate_img_root, img_base64, qos=1)
        print("FROM: "+msg.topic+" OP: "+msg.payload.decode('utf-8')+" DO: IMG SUCCESS")
    except:
      #若JSON回傳值中無result則回復沒有車牌
      print("NO PLATE")

#建立MQTT連線
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(host_local, 1883, 60)
client.loop_forever()



# d = time.strftime("%Y_%m_%d-%H_%M_%S")
# webcam_command = "fswebcam "+d+".jpg"
#忽略前20幀，捕捉第21幀影像並存至指定位置
# webcam_command = "fswebcam  -r 640x480 -S 20 --save /root/RTSP/alpr.jpg -q"
# subprocess.Popen(webcam_command, shell=True)

#休息2秒待確定檔案寫入
# time.sleep(2)

#讀取捕獲之圖片檔，投入辨識並回傳JSON
# alpr_command = "alpr -c us /root/RTSP/6F5297.jpeg -j"
# lp_data = json.loads(subprocess.check_output(alpr_command, shell=True).decode(sys.stdout.encoding))

# while True:
#   try:
#     #試將JSON中result的車牌值設給lp_number
#     lp_number = lp_data["results"][0]['plate']
#     #將JSON中result的epohtime值設給ID
#     #lp_id = lp_data["epoch_time"]
#     client.publish("PLATE/", lp_number)
#     print("PLATE:", lp_number)
  
#   except:
#     #若JSON回傳值中無result則回復沒有車牌
#     print("NO PLATE")
  
#   time.sleep(3)

#
