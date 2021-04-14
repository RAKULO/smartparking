#!/usr/bin/python
import time
import os
import datetime
import subprocess
import json
import sys

# d = time.strftime("%Y_%m_%d-%H_%M_%S")
# webcam_command = "fswebcam "+d+".jpg"
#忽略前20幀，捕捉第21幀影像並存至指定位置
webcam_command = "fswebcam  -r 640x480 -S 20 --save /root/RTSP/alpr.jpg -q"
subprocess.Popen(webcam_command, shell=True)

#休息2秒待確定檔案寫入
time.sleep(2)

#讀取捕獲之圖片檔，投入辨識並回傳JSON
alpr_command = "alpr -c us /root/RTSP/alpr.jpg -j"
lp_data = json.loads(subprocess.check_output(alpr_command, shell=True).decode(sys.stdout.encoding))

try:
  #試將JSON中result的車牌值設給lp_number
  lp_number = lp_data["results"][0]['plate']
  #將JSON中result的epohtime值設給ID
  lp_id = lp_data["epoch_time"]
  print("ID:", lp_id, "   ", "PLATE:", lp_number)
  
except:
  #若JSON回傳值中無result則回復沒有車牌
  print("NO PLATE")
