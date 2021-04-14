#!/usr/bin/python
import time
import subprocess
import json
import sys
import base64
import paho.mqtt.client as mqtt
from datetime import datetime
from retry import retry

#define topic & IP address
topic_command_root = "SERVER/off"
plate_root_out = "PLATE/out"
host = "220.132.124.155"
host_local = "broker.emqx.io"

#建立連線並設定訂閱topic
def on_connect(client, userdata, flags, rc):
  print("Connected with result code "+ str(rc))
  client.subscribe(topic_command_root)

@retry()#retry裝飾，若偵測不到車牌則不斷重複執行
#收到sever傳來的message後執行相應處理
def on_message(client, userdata, msg):
  MSG = msg.payload.decode('utf-8')

  #如果收到0則不做處理
  if MSG == "0":

  # 列印DO NOT DO ANYTHIG在console
    print("FROM: "+msg.topic+" OP: "+msg.payload.decode('utf-8')+" DO: "+"DO NOT DO ANYTHING")

  #如果收到1則拍照、辨識車牌、回傳車牌值及車牌圖片值
  elif MSG == "1":

    #給定本地當前時間
    d = datetime.now().strftime("%Y_%m_%d-%H_%M")
    
    # 忽略前20幀，捕捉第21幀影像以d值命名，並存至指定路徑
    webcam_command = "fswebcam  -r 640x480 -S 20 --save /root/RTSP/img/" + d + ".jpg -q"
    subprocess.Popen(webcam_command, shell=True)

    #休息1秒待確定檔案寫入
    time.sleep(1)

    # 讀取捕獲之圖片檔，投入辨識並獲取JSON
    alpr_command = "alpr -c us /root/RTSP/img/" + d + ".jpg -j" 
    lp_data = json.loads(subprocess.check_output(alpr_command, shell=True).decode(sys.stdout.encoding))

    #試將JSON中result的車牌值設給lp_number
    lp_number = lp_data["results"][0]['plate']

    #送出車牌值給server
    client.publish(plate_root_out, lp_number, qos=0)
    print("FROM: "+msg.topic+" OP: "+msg.payload.decode('utf-8')+" DO: "+lp_number)

def main():

  #建立MQTT連線
  client = mqtt.Client()
  client.on_connect = on_connect
  client.on_message = on_message
  client.connect(host, 1883, 60)
  client.loop_forever()

if __name__ == '__main__':
    main()