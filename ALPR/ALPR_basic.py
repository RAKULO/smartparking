#!/usr/bin/python
import time
import os
import datetime
import subprocess
import json


# d = time.strftime("%Y_%m_%d-%H_%M_%S")
# webcam_command = "fswebcam "+d+".jpg"
webcam_command = "fswebcam  -r 640x480 -S 20 --save /root/RTSP/alpr.jpg -q"
os.system(webcam_command)

time.sleep(1)

alpr_command = "alpr -c us /root/RTSP/alpr.jpg"
os.system(alpr_command)

