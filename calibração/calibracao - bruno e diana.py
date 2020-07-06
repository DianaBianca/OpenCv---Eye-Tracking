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
############################## DETECÇÂO DE PUPILA ################################

class vetorEyes:
    eyes = []

    def setVet(self, x, y):
        self.eyes.append([int(x), int(y)])
        #print(self.eyes)

    def getVet(self):
        return self.eyes

    def tamanho(self):
        return self.eyes.__len__()

################################ FUNCTIONS ######################################
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
                    pass
                    #showDetectedPupil(image, threshold, ellipses, centers, bestPupilID)

    return ellipses, centers, bestPupilID
############################## FIM DETECÇÂO DE PUPILA ######################################
#recebe um indice do vetor e retorna a media e o desvio padrão dos valores x e y
def valores(vet):
    j = 0

    coordX=[]
    coordY = []
    
    while j < 60 :
        coordX.append(vet[j][0])
        j += 1

    mediaX = int(np.mean(coordX))
    dpX = int(np.std(coordX))
    j = 0
    
    while j < 60:
        coordY.append(vet[j][1])
        j += 1

    mediaY = int(np.mean(coordY))
    dpY = int(np.std(coordY))

    return mediaX, dpX, mediaY,dpY

#recebe um indice do  vetor olhos (de 0 a 8) já com os outliners removidos e retorna a media dos valores x e y
def mediaFinal(vet):
    cdX = []
    cdY = []
    j = 0
    while j < vet.__len__():
        cdX.append(vet[j][0])
        j+=1
    mediaX = int(np.mean(cdX))

    j=0
    while j < vet.__len__():
        cdY.append(vet[j][1])
        j+=1
    mediaY = int(np.mean(cdY))
    z = 1
    return mediaX ,mediaY, z

# Define the trackbars.
trackbarsValues = {}
trackbarsValues["threshold"] = 75
trackbarsValues["minimum"] = 13
trackbarsValues["maximum"] = 32
# trackbarsValues["area"]  = 5

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
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
#pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

nextx = int(sizeX / 2) - 20
nexty = int(sizeY / 2) - 20

# nome da janela
pygame.display.set_caption("Calibração")

#GET POSITION
def _getPupilVector():
    vet = []
    done = True
    x = 0
    while done:
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
        # Draw the best pupil candidate:
        if (bestPupilID is not None and bestPupilID != -1):
            pupil = ellipses[bestPupilID]
            center = centers[bestPupilID]
            if center[0] != -1 and center[1] != -1:
                vet.append([int(center[0]), int(center[1])])
                x += 1
        if (x == 60):
            carregado = False
            x = 0
            return vet

class vetorTargets:
    
    target = []

    def setVet(self, px, py):
        self.target.append([int(px), int(py)])
        #print(self.target)

    def getVet(self):
        return self.target

## INICIO ANIMAÇÃO COM DETECÇÃO DA PUPILA ##

i = 0
py = 0
px = 0
direita = True
voltar = False
done = False
#vet = vetorTargets()
targetscoord = []
eyes = []
for x in range(9):
    
    if(i == 0):
        px = 0
        py = 0
    if(i == 1):
        px += nextx
    if(i == 2):
        px += nextx
    if (i == 3):
        py += nexty
    if (i == 4):
        px -= nextx
    if (i == 5):
        px = 0
    if (i == 6):
        py += nexty
    if (i == 7):
        px += nextx
    if (i == 8):
        px += nextx
        
    screen.fill(BLACK)
    pygame.draw.rect(screen, (255, 255, 0), [px, py, 40, 40])
    pygame.display.flip()
    #time.sleep(2)
    #CAPTURA 60 POSIÇÕES NO PONTO ATUAL DA ANIMAÇÃO
    eyes.append(_getPupilVector())
    targetscoord.append([px,py])
    i+= 1;
pygame.quit()

#coordenadas dos targets da animação
targets = np.array(np.asarray(targetscoord))
coordX = []

#recebe a media e desvio padrao de x e y de cada um dos 9 indices e elimina os outliners
for i in range(0,9):

    mediax, dpx, mediay,dpy = valores(eyes[i])
    maxX = mediax + (dpx * 1)
    minX = mediax - (dpx * 1)
    maxY = mediay + (dpy * 1)
    minY = mediay - (dpy * 1)

    j = 0
    
    for indice in eyes[i]:
        x = int(eyes[i][j][0])
        y = int(eyes[i][j][1])

        if ((x < minX or x > maxX) or (y < minY or y > maxY)):
            eyes[i].pop(j)

        j+=1
    

#criando um dicionario de cores para os 9 indices
cores = {0:'purple',1:'green',2:'orange',3:'yellow',4:'pink',5:'blue', 6:'violet',7:'brown',8:'salmon'}
#plotando os indices no grafico

for i in range(0,9):
    j = 0
    for indice in eyes[i]:
        
        x = int(eyes[i][j][0])
        y = int(eyes[i][j][1])
            
        plt.scatter(x, y, color=cores[i], s=60)
        
        j +=1 
    
eyescoord = []
#media final de todos os indices do array de olhos recebidos da função mediaFinal e transformando em um unico valor(x,y)
#print('tamanho -->', teste.__len__())

for i in range(0,9):
    x,y,z = mediaFinal(eyes[i])
    eyescoord.append([x,y])
print('tamanho -->', eyescoord.__len__())
print(eyescoord)

for i in range(0,9):
    
    x = int(eyescoord[i][0])
    y = int(eyescoord[i][1])
            
    plt.scatter(x, y, color='black', s=50)
        
       

#transformando em array os valores da lista de coordenadas
#targetEyes = np.array(np.asarray(eyescoord))

tamanhofixo = 60  # tamanho dos targets
plt.scatter(targets[:, 0], targets[:, 1], color='red', s=60)

plt.xlabel("x")
plt.ylabel("y")
plt.show()
