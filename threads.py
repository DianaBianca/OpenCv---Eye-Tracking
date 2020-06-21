import threading
import time
import cv2
import math
import numpy as np
import pygame
import ctypes
import time
import os
import matplotlib.pyplot as plt



class vetorTargets:
   target = []  

   def setVet(self, px,py):
      self.target.append([int(px), int(py)])
      print(self.target)
     
   def getVet(self):
      return self.target


class myThread (threading.Thread):
   global vet 
   def __init__(self, threadID, name, counter):
      threading.Thread.__init__(self)
      self.threadID = threadID
      self.name = name
      self.counter = counter
      
   def run(self):
      
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
              
              #print("inicio  ", vet.getVet())
              #time.sleep(5) #tempo para a calibração de cada ponto

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
          
          
          done = True
          pygame.quit()
          print("cabou")
      global vetTarget
      vetTarget = vet.getVet()

   
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

done = False

# Create new threads
thread1 = myThread(1, "Thread-1", 1)

# Start new Threads
(thread1.start())


# Add threads to thread list
threads.append(thread1)

# Wait for all threads to complete
for t in threads:
    t.join()
print ("Exiting Main Thread")

targets = np.array(np.asarray(vetTarget))
print("teste",teste)
#coordenadas  = np.array(np.asarray(vetorTargets.getVet()))

