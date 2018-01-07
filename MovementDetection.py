import argparse
import datetime
import imutils
import math
import cv2
import numpy as np
import djstatus

from tkinter import *

import time

class diffDetection:

  sec = 4   # number of seconds
  width = 800

  textIn = 0
  textOut = 0
  
  oldFrame = None
  newFrame = None
  
  maxChanged = 0  # max number of changed pixels
  maxErr = 0  # max percentage of changed pixels
  meanError = 0 # mean percentage of changed pixels
  errorSum = 0  
  frameCount = 1

  __changes = []
  __change_times = []

  __compareFrame = None

  __blur = 1
  __gauss1 = 20
  __gauss2 = 60

  def __init__(self, seconds = 4):
    self.sec = seconds

  # Returns the mean error for an interval
  def getMeanError(self):
    return self.meanError
  
  # Sets a new evaluation interval
  def setInterval(self,interval):
    if(int(interval) > 0):
      self.sec = int(interval)  

  # Option 1: Mean Squared Error
  def mse(self,imageA, imageB):
    # the 'Mean Squared Error' between the two images is the
    # sum of the squared difference between the two images;
    # NOTE: the two images must have the same dimension
    err = np.sum((imageA.astype("float") - imageB.astype("float")) ** 2)
    err /= float(imageA.shape[0] * imageA.shape[1])
    
    # return the MSE, the lower the error, the more "similar"
    # the two images are
    return err
  
  # Option 2: Bitwise difference between images
  # ti: last, current, next image
  def diffImg(self,t0, t1, t2):
    d1 = cv2.absdiff(t2, t1)
    d2 = cv2.absdiff(t1, t0)
    return cv2.bitwise_and(d1, d2)

  # Option 3: Pixelwise difference between images
  def diffPix(self, imageA, imageB):
    err = 0
    for x in range(imageA.shape[0]):
      for y in range(imageA.shape[1]):
        if(imageA[x,y] != imageB[x,y]):         
          err += 1  
    #return (err/float(imageA.shape[0]*imageA.shape[1]))
    if err > self.maxChanged:
      self.maxChanged = err
    return (err/float(self.maxChanged))

  def moodColor(self, frame):
    bgcolor = [192,0,0]
    if self.meanError > 0.7 and self.meanError < 0.9:
      bgcolor = [192,192,0]
    elif self.meanError >= 0.9:
      bgcolor = [0, 192, 0]
    
    for x in range(frame.shape[0]):
      for y in range(frame.shape[1]):
        if frame[x,y][0] == 0 and frame[x,y][1] == 0 and frame[x,y][2] == 0:
          frame[x,y] = bgcolor
        else:
          frame[x,y] = [0,0,0]

  def grabFrame(self):
    camera = cv2.VideoCapture(0)
    while True:
      (grabbed, frame) = camera.read()
      if not grabbed:
        print("  @M Waiting for camera ...")
        time.sleep(1)
        continue
      
      frame = imutils.resize(frame, width=self.width)
      frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
      frame = cv2.GaussianBlur(frame, (self.__blur, self.__blur), 0)
      frame = cv2.Canny(frame, self.__gauss1, self.__gauss2)
      
      cv2.putText(frame, "Press Q to take as first frame - WS,AD,RF to change Parameters", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
      cv2.putText(frame, str(self.__gauss1), (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
      cv2.putText(frame, str(self.__gauss2), (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
      cv2.putText(frame, str(self.__blur), (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
      cv2.imshow("Choose Empty Frame", frame)
    
      key = cv2.waitKey(1) & 0xFF
    
      if key == ord('q'):
        break
      elif key == ord('w'):
        self.__gauss1 += 10
      elif key == ord('s'):
        self.__gauss1 -= 10
      elif key == ord('a'):
        self.__gauss2 -= 10
      elif key == ord('d'):
        self.__gauss2 += 10
      elif key == ord('r'):
        self.__blur += 2
      elif key == ord('f') and self.__blur > 1:
        self.__blur -= 2
    
    self.__compareFrame = frame
    camera.release()
    cv2.destroyAllWindows() 
    

  # loop over the frames of the video
  def run(self):  
    # camera = cv2.VideoCapture("test2.mp4")
    camera = cv2.VideoCapture(0)
    firstFrame = None
  
    window = Tk()
    window.geometry("512x512")
    window.title("Feedback")
    #labeltext = StringVar()
    label = Label(window, text='X')
    label.pack()
    #window.mainloop()
  
    while True: 
      # grab the current frame and initialize the occupied/unoccupied
      # text
      (grabbed, frame) = camera.read()
      text = "Unoccupied"
    
      # if the frame could not be grabbed, then we have reached the end
      # of the video
      if not grabbed:
        break
  
      # resize the frame, convert it to grayscale, and blur it
      frame = imutils.resize(frame, width=self.width)
      gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
      gray = cv2.GaussianBlur(gray, (self.__blur, self.__blur), 0)
    
      # edge detection
      gray = cv2.Canny(gray, self.__gauss1, self.__gauss2)
  
      # >>> NEW: MSE
      error = 0
      
      if not self.__compareFrame is None:
        error = self.diffPix(gray, self.__compareFrame)
        if error > self.maxErr:
          self.maxErr = error
        self.errorSum += error
      else:
        if not self.oldFrame is None:
          self.newFrame = gray
          #error = self.mse(self.oldFrame, self.newFrame)
          error = self.diffPix(self.oldFrame, self.newFrame)
          self.oldFrame = self.newFrame
          if error > self.maxErr:
            self.maxErr = error
            #print("-M Max error: " + str(self.maxErr))
          self.errorSum += error
        else:
          self.oldFrame = gray
      
      current_time = time.time()
      self.__changes.append(error)
      self.__change_times.append(current_time)      
      
      for i in range(len(self.__changes) - 1, -1, -1):
        if current_time - self.__change_times[i] > self.sec:
          del self.__changes[i]
          del self.__change_times[i]
      
      fps = float(len(self.__changes)) / self.sec
      
      mood = 0.0
      for error in self.__changes:
        mood += error
      mood = mood / len(self.__changes)
      self.meanError = mood
      djstatus.webcam_mood(mood)
      

      # self.frameCount += 1
      # if(self.frameCount == self.sec*24):
        # self.meanError = self.errorSum/self.frameCount
        # self.errorSum = 0
        # self.frameCount = 1
        # djstatus.webcam_mood(self.meanError)
        # #print ("Mean error: " + str(self.meanError))
      
      if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
      frame = gray # black white or color ? 
      
      cv2.putText(frame, "Current error: {}".format(str(error)), (10, 30),
                  cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
      cv2.putText(frame, "Mean error (24 frames): {}".format(str(self.meanError)), (10, 50),
                  cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
      cv2.putText(frame, "Max error: {}".format(str(self.maxErr)), (10, 70),
                  cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
      cv2.putText(frame, "FPS: {}".format(str(fps)), (10, 90),
                  cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
      #show = cv2.cvtColor(frame, cv2.COLOR_GRAY2RGB)
      #self.moodColor(show)
#      cv2.imshow("Security Feed", frame)
    
      if self.meanError > 0.7 and self.meanError < 0.9:
        window.configure(background='yellow')
      elif self.meanError >= 0.9:
        window.configure(background='green')
      else:
        window.configure(background='red')
      
      #labeltext = 'Song: ' + str(djstatus.get_song()) + "\n" + 'FPS: ' + str(fps) + "\n" + 'Vote: ' + str(djstatus.get_vote())
      ltext = 'Song: ' + str(djstatus.get_song()) + "\n" + 'FPS: ' + str(fps) + "\n" + 'Vote: ' + str(djstatus.get_vote()) + "\n" + 'Mood: ' + str(mood)
      label.config(text = ltext)
      #label.pack()
      #window.update_idletasks()
      window.update()
      
      #
      #self.moodColor(show)
    
    # cleanup the camera and close any open windows
    camera.release()
    cv2.destroyAllWindows() 

#d = diffDetection()
#d.run()
  
