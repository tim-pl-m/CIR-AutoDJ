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
  
  
  votestatus = djstatus.get_votestats()
  
  print(str(votestatus[0]) + " :: " + str(votestatus[1]))
  
  
  time.sleep(1)
