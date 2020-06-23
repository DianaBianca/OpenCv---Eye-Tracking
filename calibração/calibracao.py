
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

#################################THREAD ANIMAÇÂO####################################

class vetorTargets:
    target = []

    def setVet(self, px, py):
        self.target.append([int(px), int(py)])
        print(self.target)

    def getVet(self):
        return self.target


class myThread(threading.Thread):
    global vet

    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter

    def run(self):
        global pause
        i = 2
        py = 0
        px = 0
        direita = True
        voltar = False
        done = False
        vet = vetorTargets()
        while done == False:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
            dt = clock.tick(20)

            while i != 11:

                event = pygame.event.poll()

                if event.type == pygame.QUIT:
                    break
                screen.fill(BLACK)

                pygame.draw.rect(screen, (255, 255, 0), [px, py, 40, 40])

                pygame.display.flip()

                vet.setVet(px, py)

                pause = True
                time.sleep(5) #tempo para a calibração de cada ponto
                pause = False

                if (i < 4):
                    px += nextx

                elif (i < 7):
                    if (i == 4):
                        #print('i == 4')
                        py += nexty - 20

                    else:
                        px -= nextx

                elif (i > 6):
                    if (i == 7):
                        py += nexty - 30
                        #print('i == 7')

                    else:
                        px += nextx
                i += 1

            done = True

        global vetTarget
        vetTarget = vet.getVet()

############################### FIM THREAD ANIMAÇÂO ####################################


############################## DETECÇÂO DE PUPILA ######################################
class vetorEyes:
    eyes = []

    def setVet(self, x, y):
        self.eyes.append([int(x), int(y)])
        #print(self.eyes)

    def getVet(self):
        return self.eyes

    def tamanho(self):
        return self.eyes.__len__()

################################ FUNCTIONS #####################################
def onValuesChange(self, dummy=None):
    """ Handle updates when slides have changes."""
    global trackbarsValues
    trackbarsValues["threshold"] = cv2.getTrackbarPos("threshold", "Trackbars")
    trackbarsValues["minimum"]   = cv2.getTrackbarPos("minimum", "Trackbars")
    trackbarsValues["maximum"]   = cv2.getTrackbarPos("maximum", "Trackbars")

def showDetectedPupil(image, threshold, ellipses=None, centers=None, bestPupilID=None):
    """"
    Given an image and some eye feature coordinates, show the processed image.
    """
    # Copy the input image.
    eyes = vetorEyes()
    global done
    done = False

    processed = image.copy()
    if (len(processed.shape) == 2):
        processed = cv2.cvtColor(processed, cv2.COLOR_GRAY2BGR)

    # Draw the best pupil candidate:
    if (bestPupilID is not None and bestPupilID != -1):
        pupil = ellipses[bestPupilID]
        center = centers[bestPupilID]

        cv2.ellipse(processed, pupil, (0, 255, 0), 2)

        if center[0] != -1 and center[1] != -1:
            cv2.circle(processed, (int(center[0]), int(center[1])), 5, (0, 255, 0), -1)
            #if pause == False :
            eyes.setVet(int(center[0]), int(center[1]))

            if (eyes.tamanho() >= 540):
                print(" 540 indices ok ")
                done = True
        if done == True:

            print("Acabou o laço")
            global vetEyes
            vetEyes = eyes.getVet()


    # Show the processed image.
    cv2.imshow("Detected Pupil", processed)


def detectPupil(image, threshold=101, minimum=5, maximum=50):
    """
    Given an image, return the coordinates of the pupil candidates.
    """
    # Create the output variable.
    bestPupilID = -1
    ellipses = []
    centers = []
    area = []

    kernel = np.ones((5, 5), np.uint8)

    # Grayscale image.
    grayscale = image.copy()
    if len(grayscale.shape) == 3:
        grayscale = cv2.cvtColor(grayscale, cv2.COLOR_BGR2GRAY)

    # Define the minimum and maximum size of the detected blob.
    minimum = int(round(math.pi * math.pow(minimum, 2)))
    maximum = int(round(math.pi * math.pow(maximum, 2)))

    blur = cv2.bilateralFilter(grayscale, 9, 40, 40)

    # Create a binary image.
    _, thres = cv2.threshold(blur, threshold, 255, cv2.THRESH_BINARY_INV)

    cls = cv2.morphologyEx(thres, cv2.MORPH_OPEN, kernel, iterations=1)

    # Find blobs in the input image.
    contours, hierarchy = cv2.findContours(thres, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    minRect = [None] * len(contours)
    minEllipse = [None] * len(contours)
    BestCircularity = 0

    for cnt in contours:
        prop = IAMLTools.getContourProperties(cnt, properties=["Area", "Centroid"])

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
        curva = cv2.arcLength(cnt, True)

        if (abs(1. - circularity) < abs(1. - BestCircularity)):

            BestCircularity = circularity
            bestPupilID = len(ellipses) - 1

            if (BestCircularity == circularity):
                if ((area > 3000 and area < 3900) or curva < 300):
                    showDetectedPupil(image, threshold, ellipses, centers, bestPupilID)

    # Return the final result.
    return ellipses, centers, bestPupilID
############################## FIM DETECÇÂO DE PUPILA ######################################

# Define the trackbars.
trackbarsValues = {}
trackbarsValues["threshold"] = 75
trackbarsValues["minimum"] = 13
trackbarsValues["maximum"] = 32
# trackbarsValues["area"]  = 5

# Create an OpenCV window and some trackbars.
cv2.namedWindow("Trackbars", cv2.WINDOW_AUTOSIZE)
cv2.createTrackbar("threshold", "Trackbars", 0, 255, onValuesChange)
cv2.createTrackbar("minimum", "Trackbars", 5, 40, onValuesChange)
cv2.createTrackbar("maximum", "Trackbars", 50, 100, onValuesChange)
# cv2.createTrackbar("area",  "Trackbars",  5, 400, onValuesChange)

cv2.imshow("Trackbars", np.zeros((3, 500), np.uint8))

# Create a capture video object.
filename = "inputs/eye02.mov"
capture = cv2.VideoCapture(filename)
acabou = False

threadLock = threading.Lock()
threads = []
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

# como o relógio do pygame trabalha em milissegundos, dividimos por 1000 para manter os 100 pixels por segundo
velocity = 0.05

# criamos uma instância do relógio
clock = pygame.time.Clock()

# Create new threads
thread1 = myThread(1, "Thread-1", 1)

# Start new Threads
(thread1.start())
global pause
# Add threads to thread list
threads.append(thread1)

while acabou == False:
    # Capture frame-by-frame.
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

    # Pupil detection.
    ellipses, centers, bestPupilID = detectPupil(frame, threshold, minimum, maximum)

    # Show the detected pupils.
    showDetectedPupil(frame, threshold, ellipses, centers, bestPupilID)
    if done == True:
        acabou = True
        break
    if cv2.waitKey(33) & 0xFF == ord("q"):
        break

capture.release()
cv2.destroyAllWindows()
print("olhosss -> ",vetEyes)

for t in threads:
    t.join()

pygame.quit()

targets = np.array(np.asarray(vetTarget))
eyes =  np.array(np.asarray(vetEyes))
