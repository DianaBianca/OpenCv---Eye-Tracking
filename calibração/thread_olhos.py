import threading
import time

############################ IMPORTS ############################################
import cv2
import math
import numpy as np
import IAMLTools
import imutils
import BlobProperties
import pygame
import ctypes
import time
import os
import matplotlib.pyplot as plt
import threading
#################################################################################




################################## TRACKBARS #########################################
# Define the trackbars.
trackbarsValues = {}
trackbarsValues["threshold"] = 75
trackbarsValues["minimum"]  = 13
trackbarsValues["maximum"]  = 32
#trackbarsValues["area"]  = 5

# Create an OpenCV window and some trackbars.
cv2.namedWindow("Trackbars", cv2.WINDOW_AUTOSIZE)
cv2.createTrackbar("threshold", "Trackbars",  0, 255, onValuesChange)
cv2.createTrackbar("minimum",   "Trackbars",  5,  40, onValuesChange)
cv2.createTrackbar("maximum",   "Trackbars", 50, 100, onValuesChange)

cv2.imshow("Trackbars", np.zeros((3, 500), np.uint8))

######################################################################################

# Create a capture video object.
filename = "inputs/eye02.mov"
capture = cv2.VideoCapture(filename)

class vetorEyes:
   eyes = []  

   def setVet(self, px,py):
      self.eyes.append([int(x), int(y)])
      print(self.eyes)
     
   def getVet(self):
      return self.eyes

class myThread (threading.Thread):
   def __init__(self, threadID, name, counter):
      threading.Thread.__init__(self)
      self.threadID = threadID
      self.name = name
      self.counter = counter
      
   def run(self):
      while True :
          # Get the detection parameters values.
          threshold = trackbarsValues["threshold"]
          minimum = trackbarsValues["minimum"]
          maximum = trackbarsValues["maximum"]
          retval, frame = capture.read()

          # Check if there is a valid frame.
          if not retval:
              # Restart the video.
              capture.set(cv2.CAP_PROP_POS_FRAMES, 0)
              continue

          # Pupil detection.

          ellipses, centers, bestPupilID = detectPupil(frame, threshold, minimum, maximum)

          # Show the detected pupils.
          showDetectedPupil(frame, threshold, ellipses, centers, bestPupilID)
            # Free lock to release next thread
      threadLock.release()
      
      ################################ FUNCTIONS ######################################
   def onValuesChange(self, dummy=None):
       """ Handle updates when slides have changes."""
       global trackbarsValues
       trackbarsValues["threshold"] = cv2.getTrackbarPos("threshold", "Trackbars")
       trackbarsValues["minimum"]   = cv2.getTrackbarPos("minimum", "Trackbars")
       trackbarsValues["maximum"]   = cv2.getTrackbarPos("maximum", "Trackbars")
       #trackbarsValues["area"]  = cv2.getTrackbarPos("area", "Trackbars")

   def showDetectedPupil(image, threshold, ellipses=None, centers=None, bestPupilID=None):
       """"
       Given an image and some eye feature coordinates, show the processed image.
       """

       # Copy the input image.
       processed = image.copy()
       if (len(processed.shape) == 2):
           processed = cv2.cvtColor(processed, cv2.COLOR_GRAY2BGR)

       # Draw the best pupil candidate:
       if (bestPupilID is not None and bestPupilID != -1):
           pupil  = ellipses[bestPupilID]
           center = centers[bestPupilID]

           cv2.ellipse(processed, pupil, (0, 255, 0), 2)

           if center[0] != -1 and center[1] != -1:
               cv2.circle(processed, (int(center[0]), int(center[1])), 5, (0, 255, 0), -1)

               if coordenadas.__len__() <= 540:
                  
                  coordenadas.append([int(center[0]), int(center[1])])
                  print("VALUES -----> ", int(center[0]), " , ", int(center[1]))
                  print("TAMANHO DA LISTA : ", coordenadas.__len__())
                  
               else:
                  targetEyes(coordenadas)
                  print("LISTA : ", coordenadas)
                  cv2.destroyAllWindows()


           # Show the processed image.
           cv2.imshow("Detected Pupil", processed)

       # Show the processed image.
       cv2.imshow("Detected Pupil", processed)



   def detectPupil(image, threshold=101, minimum=5, maximum=50):
       """
       Given an image, return the coordinates of the pupil candidates.
       """
       # Create the output variable.
       bestPupilID = -1
       ellipses    = []
       centers     = []
       area        = []

       kernel  = np.ones((5,5),np.uint8)

       # Grayscale image.
       grayscale = image.copy()
       if len(grayscale.shape) == 3:
           grayscale = cv2.cvtColor(grayscale, cv2.COLOR_BGR2GRAY)


       # Define the minimum and maximum size of the detected blob.
       minimum = int(round(math.pi * math.pow(minimum, 2)))
       maximum = int(round(math.pi * math.pow(maximum, 2)))

       blur= cv2.bilateralFilter(grayscale,9,40,40)

       # Create a binary image.
       _, thres = cv2.threshold(blur, threshold, 255,cv2.THRESH_BINARY_INV)

       cls = cv2.morphologyEx(thres,cv2.MORPH_OPEN,kernel, iterations = 1)

       # Show the threshould image.
       cv2.imshow("Threshold", thres)

       # Find blobs in the input image.
       contours, hierarchy= cv2.findContours(thres, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

       #<!--------------------------------------------------------------------------->
       #<!--                            YOUR CODE HERE                             -->
       #<!--------------------------------------------------------------------------->

       minRect = [None]*len(contours)
       minEllipse = [None]*len(contours)
       BestCircularity = 0

       for cnt in contours:
           prop = IAMLTools.getContourProperties(cnt, properties=["Area","Centroid"])

           if len(cnt) > 5:
               ellipse = cv2.fitEllipse(cnt)
           else:
               ellipse = cv2.minAreaRect(cnt)

           area = prop["Area"]
           center = prop["Centroid"]

           if (area < minimum or area > maximum):
               continue

           ellipses.append(ellipse)
           centers.append(center)

           prop = IAMLTools.getContourProperties(cnt, ["Circularity"])
           circularity = prop["Circularity"]
           curva = cv2.arcLength(cnt,True)
          # print("curvatura",curva)
          # print("circulo  ",circularity)
          # print("area  ",area)

           if(abs(1. - circularity) < abs(1. - BestCircularity)):

               BestCircularity = circularity
               bestPupilID = len(ellipses)-1

               if(BestCircularity == circularity):
                   if((area > 3000 and area < 3900)  or curva < 300):
                        showDetectedPupil(image, threshold, ellipses, centers , bestPupilID)


       #<!--------------------------------------------------------------------------->
       #<!--                                                                       -->
       #<!--------------------------------------------------------------------------->

       # Return the final result.
       return ellipses, centers, bestPupilID


   ######################################################################################


threadLock = threading.Lock()
threads = []

# Create new threads
thread1 = myThread(1, "Thread-1", 1)

# Start new Threads
thread1.start()

# Add threads to thread list
threads.append(thread1)

# Wait for all threads to complete
for t in threads:
    t.join()

