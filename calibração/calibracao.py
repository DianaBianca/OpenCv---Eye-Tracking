import pygame
import ctypes
import time
import os
import numpy as np
import cv2
import numpy as np
import matplotlib.pyplot as plt

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

# -------- Main Program Loop -----------

while done == False:
    for event in pygame.event.get():  # User did something
        if event.type == pygame.QUIT:  # If user clicked close
            done = True  # Flag that we are done so we exit this loop

    # chamamos o tick do relógio para 30 fps e armazenamos o delta de tempo
    dt = clock.tick(20)

    while i != 11:

        event = pygame.event.poll()

        if event.type == pygame.QUIT:
            break
        screen.fill(BLACK)

        pygame.draw.rect(screen, (255, 255, 0), [px, py, 40, 40])

        pygame.display.flip()

        coordenadas.append([int(px), int(py)])

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
