
__version__ = "$Revision: 2018031201 $"

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
#################################################################################


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
            print("VALUES -----> ",int(center[0]), " , " ,int(center[1]))

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
        print("curvatura",curva)
        print("circulo  ",circularity)
        print("area  ",area)
        
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

# como o relógio do pygame trabalha em milissegundos, dividimos por 1000 para manter os 100 pixels por segundo
velocity = 0.05

# criamos uma instância do relógio
clock = pygame.time.Clock()

#armazena as coordenadas da animação
coordenadas = []
eyes = []

run = True
while run == True:
    # -------- Main Program Loop -----------

    retval, frame = capture.read()

    # Check if there is a valid frame.
    if not retval:
        # Restart the video.
        capture.set(cv2.CAP_PROP_POS_FRAMES, 0)
        continue

    # Get the detection parameters values.
    threshold = trackbarsValues["threshold"]
    minimum = trackbarsValues["minimum"]
    maximum = trackbarsValues["maximum"]
    # area  = trackbarsValues["area"]

    # Pupil detection.
    ellipses, centers, bestPupilID = detectPupil(frame, threshold, minimum, maximum)

    # Show the detected pupils.
    showDetectedPupil(frame, threshold, ellipses, centers, bestPupilID)

while done == False:
    for event in pygame.event.get():  # User did something
        if event.type == pygame.QUIT:  # If user clicked close
            done = True  # Flag that we are done so we exit this loop

    # chamamos o tick do relógio para 30 fps e armazenamos o delta de tempo
    dt = clock.tick(20)

         # Capture frame-by-frame.

    while i != 11:

        event = pygame.event.poll()

        if event.type == pygame.QUIT:
            break
        screen.fill(BLACK)

        pygame.draw.rect(screen, (255, 255, 0), [px, py, 40, 40])

        pygame.display.flip()


        coordenadas.append([int(px), int(py)])

        time.sleep(5) #tempo para a calibração de cada ponto

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
    done = True
    # Close the window and quit.
    pygame.quit()

print(coordenadas)
#coordenadas dos targets da animação
targets = np.array(np.asarray(coordenadas))
print(targets)

#coordenadas dos olhos
eyes = np.array([[0, 0, 1],
                 [0.25, 0, 1],
                 [0.5, 0, 1],
                 [0, 0.25, 1],
                 [0.25, 0.25, 1],
                 [0.5, 0.25, 1],
                 [0, 0.50, 1],
                 [0.25, 0.50, 1],
                 [0.5, 0.50, 1]])

tamanhofixo = 60  # tamanho dos targets

# plt.scatter(eyes[:,0],eyes[:,1], color='blue', s=tamanhofixo)
plt.scatter(targets[:, 0], targets[:, 1], color='red', s=tamanhofixo)

equation = np.ones((9, 6))  # 6 equações e 9 alvos

# pegar cada coordenada do olho e realizar a equação
for i, eye in enumerate(eyes):
    equation[i, :-1] = [eye[0] ** 2, eye[1] ** 2, eye[0] * eye[1], eye[0], eye[1]]

coeffsX = np.linalg.pinv(equation).dot(targets[:, 0])
coeffsY = np.linalg.pinv(equation).dot(targets[:, 1])

M = np.vstack((coeffsX, coeffsY))

eye = np.array([0.25, 0.15])

# Gaze estimation method
gaze = M.dot([eye[0] ** 2, eye[1] ** 2, eye[0] * eye[1], eye[0], eye[1], 1])

print(gaze)

a = gaze[0]
b = gaze[1]

plt.scatter(a, b, color='black', s=200)

plt.xlabel("x")
plt.ylabel("y")
plt.show()
