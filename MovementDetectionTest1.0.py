import argparse
import datetime
import imutils
import math
import cv2
import numpy as np

class diffDetection:

	sec = 1		# number of seconds
	width = 800

	textIn = 0
	textOut = 0
	
	oldFrame = None
	newFrame = None

	maxErr = 0
	meanError = 0
	errorSum = 0
	frameCount = 1

	# Option 1: Mean Squared Error
	def mse(imageA, imageB):
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
	def diffImg(t0, t1, t2):
		d1 = cv2.absdiff(t2, t1)
		d2 = cv2.absdiff(t1, t0)
		return cv2.bitwise_and(d1, d2)
	
	# camera = cv2.VideoCapture("test2.mp4")
	camera = cv2.VideoCapture(0)
	
	firstFrame = None

	# loop over the frames of the video
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
	    frame = imutils.resize(frame, width=width)
	    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	    #gray = cv2.GaussianBlur(gray, (21, 21), 0)
		
	    # edge detection
	    gray = cv2.Canny(gray,100,200)
	
	    # >>> NEW: MSE
	    error = 0
	    if not oldFrame is None:
		newFrame = gray
		error = mse(oldFrame, newFrame)
		oldFrame = newFrame
		if error > maxErr:
			maxErr = error
			print ("Max error: " + str(maxErr))
		errorSum += error
	    else:
		oldFrame = gray

	    frameCount += 1
	    if(frameCount == sec*24):
		meanError = errorSum/sec*24
		errorSum = 0
		frameCount = 1
		print ("Mean error: " + str(meanError))
	
	    if cv2.waitKey(1) & 0xFF == ord('q'):
	        break
	
	    frame = gray # black white or color ? 
		
	    cv2.putText(frame, "Current error: {}".format(str(error)), (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
	    cv2.putText(frame, "Mean error (24 frames): {}".format(str(meanError)), (10, 50),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
	    cv2.putText(frame, "Max error: {}".format(str(maxErr)), (10, 70),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
	    cv2.imshow("Security Feed", frame)

	# cleanup the camera and close any open windows
	camera.release()
	cv2.destroyAllWindows()
