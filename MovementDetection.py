import argparse
import datetime
import imutils
import math
import cv2
import numpy as np
import djstatus

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
  
  

  # loop over the frames of the video
  def run(self):  
    # camera = cv2.VideoCapture("test2.mp4")
    camera = cv2.VideoCapture(0)
    firstFrame = None
  
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
      #gray = cv2.GaussianBlur(gray, (21, 21), 0)
    
      # edge detection
      gray = cv2.Canny(gray,100,200)
  
      # >>> NEW: MSE
      error = 0
      if not self.oldFrame is None:
        self.newFrame = gray
        #error = self.mse(self.oldFrame, self.newFrame)
        error = self.diffPix(self.oldFrame, self.newFrame)
        self.oldFrame = self.newFrame
        if error > self.maxErr:
          self.maxErr = error
          print ("Max error: " + str(self.maxErr))
        self.errorSum += error
      else:
        self.oldFrame = gray
    
      self.frameCount += 1
      if(self.frameCount == self.sec*24):
        self.meanError = self.errorSum/self.frameCount
        self.errorSum = 0
        self.frameCount = 1
        djstatus.webcam_mood(self.meanError)
        #print ("Mean error: " + str(self.meanError))
      
      if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
      frame = gray # black white or color ? 
      
      cv2.putText(frame, "Current error: {}".format(str(error)), (10, 30),
                  cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
      cv2.putText(frame, "Mean error (24 frames): {}".format(str(self.meanError)), (10, 50),
                  cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
      cv2.putText(frame, "Max error: {}".format(str(self.maxErr)), (10, 70),
                  cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
      cv2.imshow("Security Feed", frame)
    
    # cleanup the camera and close any open windows
    camera.release()
    cv2.destroyAllWindows() 

#d = diffDetection()
#d.run()
  
