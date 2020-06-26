########################################################################
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
########################################################################

def onValuesChange(self, dummy=None):
    """ Handle updates when slides have changes."""
    global trackbarsValues
    trackbarsValues["threshold"] = cv2.getTrackbarPos("threshold", "Trackbars")
    trackbarsValues["minimum"]   = cv2.getTrackbarPos("minimum", "Trackbars")
    trackbarsValues["maximum"]   = cv2.getTrackbarPos("maximum", "Trackbars")
    #trackbarsValues["area"]  = cv2.getTrackbarPos("area", "Trackbars")

def valores(vet):
    print(vet)
    #return vetTarget

    # tela cheia
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    pygame.init()

    # Define algumas cores colors
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)

    # Seta a largura e a altura da tela utilizada [width, height](só funciona para windows)
    user32 = ctypes.windll.user32

    # 1366 768- tamanho da minha tela
    sizeX = user32.GetSystemMetrics(0)
    sizeY = user32.GetSystemMetrics(1)

    size = sizeX, sizeY
    screen = pygame.display.set_mode(size)

    nextx = int(sizeX / 2) - 20
    nexty = int(sizeY / 2)

    # nome da janela
    pygame.display.set_caption("Calibração")

    # Loop until the user clicks the close button.
    done = False

    # Used to manage how fast the screen updates
    clock = pygame.time.Clock()

    i = 2
    py = 0
    px = 0
    direita = True
    voltar = False
    # como o relógio do pygame trabalha
    # em milissegundos, dividimos por 1000
    # para manter os 100 pixels por segundo
    velocity = 0.05

    # criamos uma instância do relógio
    clock = pygame.time.Clock()
    targets = []
    eyes =[]
    # -------- Main Program Loop -----------

    while done == False:
        for event in pygame.event.get():  # User did something
            if event.type == pygame.QUIT:  # If user clicked close
                done = True  # Flag that we are done so we exit this loop

        # Set the screen background
        # screen.fill(BLACK)
        # chamamos o tick do relógio para 30 fps
        # e armazenamos o delta de tempo
        dt = clock.tick(20)

        while i != 11:

            event = pygame.event.poll()

            if event.type == pygame.QUIT:
                break
            screen.fill(BLACK)

            pygame.draw.rect(screen, (255, 255, 0), [px, py, 40, 40])  #

            pygame.display.flip()
            targets.append([px,py])
            eyes.append(vet)
            #time.sleep(5)  # tempo para a calibração de cada ponto

            if (i < 4):
                px += nextx

            elif (i < 7):
                if (i == 4):
                    print('i == 4')
                    py += nexty - 20

                else:
                    px -= nextx

            elif (i > 6):
                if (i == 7):
                    py += nexty - 30
                    print('i == 7')

                else:
                    px += nextx
            i += 1

            # Close the window and quit.
    pygame.quit()


class vetorEyes:
    eyes = []

    def setVet(self, x,y):
        self.eyes.append([x,y])
        #print(self.eyes)

    def getVet(self):
        return self.eyes

    def tamanho(self):
        return self.eyes.__len__()

    def limpar(self):
        self.eyes.clear()


def showDetectedPupil(image, threshold, ellipses=None, centers=None, bestPupilID=None):
    """"
    Given an image and some eye feature coordinates, show the processed image.
    ""
    """

    global vetTarget
    eyes = vetorEyes()
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
            eyes.setVet(int(center[0]), int(center[1]))
            #print("tamanho do vetor ", eyes.tamanho())

    if eyes.tamanho() == 60:
        #print('aqui')
        vetTarget = eyes.getVet()
        valores(vetTarget)
        eyes.limpar()
    # Show the processed image.
    #cv2.imshow("Detected Pupil", processed)

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
    #cv2.imshow("Threshold", thres)
    
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
#cv2.createTrackbar("area",  "Trackbars",  5, 400, onValuesChange)

cv2.imshow("Trackbars", np.zeros((3, 500), np.uint8))

# Create a capture video object.
filename = "inputs/eye02.mov"
capture = cv2.VideoCapture(filename)

# This repetion will run while there is a new frame in the video file or
# while the user do not press the "q" (quit) keyboard button.
while True:

    # Capture frame-by-frame.
    retval, frame = capture.read()

    # Check if there is a valid frame.
    if not retval:
        # Restart the video.
        capture.set(cv2.CAP_PROP_POS_FRAMES, 0)
        continue

    # Get the detection parameters values.
    threshold = trackbarsValues["threshold"]
    minimum   = trackbarsValues["minimum"]
    maximum   = trackbarsValues["maximum"]
    #area  = trackbarsValues["area"]  
    
    # Pupil detection.
    ellipses, centers, bestPupilID = detectPupil(frame, threshold, minimum, maximum)

    # Show the detected pupils.
    x = showDetectedPupil(frame, threshold, ellipses, centers, bestPupilID)
    print("array  ", x)
    
    # Display the captured frame.
    #cv2.imshow("Eye Image", frame)
    if cv2.waitKey(33) & 0xFF == ord("q"):
        break

# When everything done, release the capture object.
capture.release()
cv2.destroyAllWindows()
cv2.destroyAllWindows()
