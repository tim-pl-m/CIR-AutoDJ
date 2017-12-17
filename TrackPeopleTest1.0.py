
import argparse
import datetime
import imutils
import math
import cv2
import numpy as np

width = 800

textIn = 0
textOut = 0

oldFrame = None
newFrame = None

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



def testIntersectionIn(x, y):

    res = -450 * x + 400 * y + 157500
    if((res >= -550) and  (res < 550)):
        print (str(res))
        return True
    return False



def testIntersectionOut(x, y):
    res = -450 * x + 400 * y + 180000
    if ((res >= -550) and (res <= 550)):
        print (str(res))
        return True

    return False

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
    gray = cv2.GaussianBlur(gray, (21, 21), 0)

	
    # >>> NEW: Detect human bodies

    # Name of the downloaded my cascades.. 
    #cascadeHead = "./cascadeH5.xml"
    cascadeName = "./cascadG.xml"

    # Load the cascade

    detectorBody = cv2.CascadeClassifier("~/Desktop/CRI-AuttoDJ/cascadG.xml")
    #detectorHead = cv2.CascadeClassifier(cascadeHead)
       
    # Detect human bodies
    bodies = detectorBody.detectMultiScale(gray, 1.3, 5)

    # >>> NEW: MSE
    error = 0
    if not oldFrame is None:
	newFrame = gray
	error = mse(oldFrame, newFrame)
	oldFrame = newFrame
    else:
	oldFrame = gray

    # if the first frame is None, initialize it
    if firstFrame is None:
        firstFrame = gray
        continue

    # compute the absolute difference between the current frame and
    # first frame
    frameDelta = cv2.absdiff(firstFrame, gray)
    thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]
    # dilate the thresholded image to fill in holes, then find contours
    # on thresholded image
    thresh = cv2.dilate(thresh, None, iterations=2)
    _, cnts, _ = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # loop over the contours
    for c in cnts:
        # if the contour is too small, ignore it
        if cv2.contourArea(c) < 12000:
            continue
        # compute the bounding box for the contour, draw it on the frame,
        # and update the text
        (x, y, w, h) = cv2.boundingRect(c)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        #cv2.line(frame, (width / 2, 0), (width, 450), (250, 0, 1), 2) #blue line
        #cv2.line(frame, (width / 2 - 50, 0), (width - 50, 450), (0, 0, 255), 2)#red line


        rectagleCenterPont = ((x + x + w) /2, (y + y + h) /2)
        cv2.circle(frame, rectagleCenterPont, 1, (0, 0, 255), 5)

        if(testIntersectionIn((x + x + w) / 2, (y + y + h) / 2)):
            textIn += 1

        if(testIntersectionOut((x + x + w) / 2, (y + y + h) / 2)):
            textOut += 1

        # draw the text and timestamp on the frame

        # show the frame and record if the user presses a key
        # cv2.imshow("Thresh", thresh)
        # cv2.imshow("Frame Delta", frameDelta)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    cv2.putText(frame, "autoDJ Test", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
    cv2.putText(frame, "In: {}".format(str(textIn)), (10, 50),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
    cv2.putText(frame, "Out: {}".format(str(textOut)), (10, 70),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
    cv2.putText(frame, "Counter: {}".format(str(len(cnts))), (10, 90),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
    cv2.putText(frame, "Error: {}".format(str(error)), (10, 110),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
    cv2.putText(frame, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"),
                (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)
    cv2.imshow("Security Feed", frame)


# cleanup the camera and close any open windows
camera.release()
cv2.destroyAllWindows()

