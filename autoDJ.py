#!/usr/bin/python3

import _thread
import spot_control
import djstatus
import webservice

import threading

import time

import MovementDetection as mvd

import learning

loop_seconds = 10

print("# Initialising Movement Detection ...")
webcam = mvd.diffDetection(loop_seconds - 1)
webcam.grabFrame()

#djstat = djstatus.djstatus()
print("# Initialising Spotify ...")
spotcontrol = spot_control.spot_control(False)

print("# Starting Threads ...")
threading.Thread(target=webservice.run).start()
threading.Thread(target=webcam.run).start()

qlearn = learning.learning()

# getRandomParamter();

print("# Enter Main-Loop ...")

wait = False
while True:

  params = qlearn.getNextParamters()

  duration = spotcontrol.play(params[0][0], params[1], params[3], params[2], wait)
  djstatus.clear_vote()

  seconds = float(duration) / 1000 - 5
  if seconds < 5:
    seconds = 5

  seconds = loop_seconds

  song = djstatus.get_song()
  
  print("# Playing " + str(song))
  print("# Sleep for " + str(seconds) + " seconds")
  time.sleep(seconds)

  votestatus = djstatus.get_votestats()
  moodstatus = djstatus.get_mood()
  allmood = moodstatus
  if votestatus[1] > 0:
    allmood += float(votestatus[0]) / votestatus[1]
    allmood = allmood / 2

  print("# Learning Feedback: " + str(allmood))
  #print(str(votestatus[0]) + " :: " + str(votestatus[1]))
  qlearn.learn(allmood)
  # parameterList = getNextParamters()
