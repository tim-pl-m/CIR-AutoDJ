#!/usr/bin/python3

import _thread
import spot_control
import djstatus
import webservice

import time


#djstat = djstatus.djstatus()

spotcontrol = spot_control.spot_control(False)

webservice.run()

while True:
  
  print("*")
  
  
  time.sleep(1)
