#!/usr/bin/python3

import _thread
import spot_control
import djstatus
import webservice

import threading

import time

import MovementDetectionTest1.0 as mvd

#djstat = djstatus.djstatus()

spotcontrol = spot_control.spot_control(False)

webcam = mvd.diffDetection()

threading.Thread(target=webservice.run()).start()
threading.Thread(target=webcam.run()).start()


# getRandomParamter();

while True:

  votestatus = djstatus.get_votestats()

  print(str(votestatus[0]) + " :: " + str(votestatus[1]))

  # parameterList = getNextParamters()


  time.sleep(1)
